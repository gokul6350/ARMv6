import cv2 as cv
from cv2 import aruco
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import marker
import math
import time
import sys
import rich



#suppress_output()
global detected_objects 
global origin
global cen
detected_objects = {}
origin = None
cen = {}
calib_data_path = "/home/gokul/Documents/armv6/ARMv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
model = YOLO("best.pt")
#print(model)
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

classNames = ["ball", "battery", "grip"]
result_dict = {"detect_obj": [], "cen": [], "frame": []}
#vid = cv.VideoCapture("/home/gokul/2024-01-27 17-26-19.mkv")
vid = cv.VideoCapture(0)

def _alert(mssg):
    rich.print(f"[bold red]alert {mssg} [/bold red]")


def detector(frame):
    cv.imshow("ORIGINAL", frame)
    results = model(frame,stream=True)
    print("====================")
    print(results)
    print("==================")

    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_name = classNames[int(box.cls[0])]
            print(class_name)
            if class_name == "battery":
                battery_found = True
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                battery_center = (cx, cy)
                cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 3)
                cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 1)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                text = f"{class_name} ({confidence})"
                cv.putText(frame, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                detected_objects[class_name] = (battery_center[0], battery_center[1])
            print(f">>>>{detected_objects}")

    return frame
def redist(corners1, corners2):
    #corners_1=tuple(map(int,corners1))
    #corners_2=tuple(map(int,corners2))
                   
    rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(corners1, MARKER_SIZE, cam_mat, dist_coef)
    rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(corners2, MARKER_SIZE, cam_mat, dist_coef)

    tvec1 = tvec1.squeeze()
    tvec2 = tvec2.squeeze()

    distance = np.linalg.norm(tvec2 - tvec1)
    print(distance)
    return distance

def prespective_transforme(frame,cen,cor):
    pts_original = np.float32([cen["cen2"],cen["cen1"],cen["cen3"],cen["cen4"]])
    wi = round(redist(cor["con1"], cor["con2"]), 1)
    le = round(redist(cor["con2"], cor["con3"]), 1)

    wi,le = wi*10 , le*10
    pts_transformed = np.float32([[0, 0], [wi, 0], [0, le], [wi, le]])
    matrix = cv.getPerspectiveTransform(pts_original, pts_transformed)
    result = cv.warpPerspective(frame, matrix, (int(wi), int(le)))
    origin=wi/2
    return result,wi/2

def cam():
    i=0
    while True:
        i=i+1
        ret, frame = vid.read()
        if not ret:
            print("Error reading frame")
            break

        frame,cen,cor= marker.detect_markers(frame)
        if frame.any():  # Check if any element in frame is True
             print("frame is not none")# Your code here
        else:
            _alert("Frame is a Nonetype")
            break

        if  cen["cen1"] == [] or cen["cen2"] == [] or cen["cen3"] == [] or cen["cen4"] == []:
            rich.print("[bold red]alert ValueError ! [/bold red] Not enough center points")
        elif len(cen) == 4:
            frame,origin=prespective_transforme(frame,cen,cor)
            cv.imshow('Frame', frame)
           # cv.waitKey(5000)
            frame=detector(frame)
        print(detected_objects)
       # cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        if i >= 5:
            if len(cen) == 4:
                if detected_objects == {}:
                    raise NotImplementedError
                vid.release()
                cv.destroyAllWindows()
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                cv.imwrite(f'logs/obj-{formatted_time}.jpg',frame)
                return detected_objects,origin,frame
                
   # enable_output()        
 


