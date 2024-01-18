import cv2 as cv
from cv2 import aruco
import numpy as np
from datetime import datetime

calib_data_path = "/home/gokul/Documents/armv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

vid = cv.VideoCapture(0)

def detect_marker(frame):
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    # Initialize the dictionary outside the loop
    _cen = {"c1": [], "c2": [], "c3": []}

    if marker_corners:
        centers = {}
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            center = tuple(map(int, np.mean(corners, axis=(1, 0))))
            
            # Check if the ID is within the range of interest (1 to 4)
            if int(ids) in range(1, 5):
                centers[int(ids)] = center

                # Store the corners in the dictionary
                if int(ids) == 1:
                    coner1 = corners.reshape(1, 4, 2)
                    _cen["c1"] = coner1
                elif int(ids) == 2:
                    coner2 = corners.reshape(1, 4, 2)
                    _cen["c2"] = coner2
                elif int(ids) == 3:
                    coner3 = corners.reshape(1, 4, 2)
                    _cen["c3"] = coner3

    return frame, _cen

def detection():
    x =0 
    while True:
        x=x+1
        ret, frame = vid.read()
        if not ret:
            break

        try:
            cv.imwrite(f'logs3/gbomba-frame(3){x}-{formatted_time}.jpg', frame)
        except Exception as e:
            print(f"Error writing image: {e}")

        #frame, object = detect_marker(frame=frame)
        #cv.imshow("frameeff", frame)
        cv.imwrite(f'logs3/gbomba-detection(3){x}-{formatted_time}.jpg', frame)

detection()
