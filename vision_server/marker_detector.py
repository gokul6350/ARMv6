import cv2 as cv
from cv2 import aruco
import numpy as np

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

    # detect the marker
param_markers = aruco.DetectorParameters()
detector12 = cv.aruco.ArucoDetector(marker_dict, param_markers)
print(detector12)
def detect_markers(frame):
 


    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = detector12.detectMarkers(gray_frame)
    cen={"cen1":[],"cen2":[],"cen3":[],"cen4":[]}
    cor={"con1":[],"con2":[],"con3":[],"con4":[]}
 
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            center = tuple(map(int, np.mean(corners, axis=(1, 0))))
            corners = corners.reshape(4, 2)
            cv.circle(frame, center, 5, (0, 255, 0), -1)
            corners1=corners
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            cv.putText(
                frame,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
            #print(f"ids:{ids}, mID:{marker_IDs}")
            if int(ids) == 6:
                cen1 = center
                cen["cen1"]=cen1
                cor["con1"]=corners1.reshape(1, 4, 2)
            elif int(ids) == 7:
                cen2 = center
                cen["cen2"]=cen2
                cor["con2"]=corners1.reshape(1, 4, 2)
            elif int(ids) == 8:
                cen3 = center
                cen["cen3"]=cen3
                cor["con3"]=corners1.reshape(1, 4, 2)
            elif int(ids) == 9:
                cen4 = center
                cen["cen4"]=cen4           
    
    return frame, cen, cor
