from flask import Flask, render_template, Response,jsonify
import cv2
from marker_detector import detect_markers
from object_detector import detector
import numpy as np
from cv2 import aruco
import base64
from io import BytesIO


app = Flask(__name__)

MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()
calib_data_path = "/home/gokul/Documents/armv6/ARMv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

objs = {}  
origin = None  
framexc=np.zeros((608, 608, 3), dtype=np.uint8)
#detector = cv2.aruco.ArucoDetector(marker_dict, param_markers)
def combine_dicts_overwrite(dict1, dict2):
    
    result = dict1.copy()  
    if isinstance(dict2, list):  
        for d in dict2:
            for key, value in d.items():
                result[key] = value  
    else:  
        for key, value in dict2.items():
            result[key] = value  
    return result


def base_64(frame):
    success, png_image = cv2.imencode('.png', frame)
    if not success:
        print("Failed to encode frame as PNG")
        exit()

# Convert PNG image to base64 encoding
    base64_text = base64.b64encode(png_image).decode('utf-8')


    return base64_text

def prespective_transforme(frame, cen, cor):
    pts_original = np.float32([cen["cen1"], cen["cen2"], cen["cen4"], cen["cen3"]])
    wi, le = 28.7 * 10, 35.7 * 10  
    pts_transformed = np.float32([[0, 0], [wi, 0], [0, le], [wi, le]])
    matrix = cv2.getPerspectiveTransform(pts_original, pts_transformed)
    result = cv2.warpPerspective(frame, matrix, (int(wi), int(le)))
    origin = wi / 2
    return result, wi / 2

def redist(corners1, corners2):
    rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(corners1, MARKER_SIZE, cam_mat, dist_coef)
    rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(corners2, MARKER_SIZE, cam_mat, dist_coef)

    tvec1 = tvec1.squeeze()
    tvec2 = tvec2.squeeze()

    distance = np.linalg.norm(tvec2 - tvec1)
    print(distance)
    return distance


    return None, None, frame    
previous_objs = {}
 
def cam(vid):
    global previous_objs, objs, origin,framexc
    objs = {}
    ret, frame = vid.read()
    if not ret:
        print("Error reading frame")
        exit()

    frame, cen, cor = detect_markers(frame)

    if cen["cen1"] == [] or cen["cen2"] == [] or cen["cen3"] == [] or cen["cen4"] == []:
        print("ValueError! Not enough center points")
        frame=framexc.copy()
        return None, None, frame
    elif len(cen) == 4:
        frame11, origin = prespective_transforme(frame, cen, cor)
        #print(frame11)
        if frame11 is not None:
           frame12, objs2 = detector(frame11)
       # print(f">>>{objs2}")
       
        objs = combine_dicts_overwrite(previous_objs, objs2)
        previous_objs = objs.copy()
        print(previous_objs)  # Update previous_objs by making a copy
        framexc=frame12.copy()
        return objs, origin, frame12
    return None, None, frame


def generate_frames():
    vid = cv2.VideoCapture(0)
    while True:
        objs, origin, frame = cam(vid)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dynamic_text')
def dynamic_text():
    global previous_objs, origin  # Access global variables
    png=base_64(framexc)
    print("REQUEST MADE >>>>>>>>>>>><<<<<<<<<<<<<")
    return jsonify({"objects": previous_objs, "origin": origin,"base64":png})


if __name__ == "__main__":
    app.run(debug=True)
