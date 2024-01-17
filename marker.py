import cv2 as cv
from cv2 import aruco
import numpy as np

def detect_markers(frame):
    # dictionary to specify type of the marker
    marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)

    # detect the marker
    param_markers = aruco.DetectorParameters()

    # turning the frame to grayscale-only (for efficiency)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    cen={"cen1":[],"cen2":[],"cen3":[],"cen4":[]}
    # getting corners of markers
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            center = tuple(map(int, np.mean(corners, axis=(1, 0))))
            corners = corners.reshape(4, 2)
            cv.circle(frame, center, 5, (0, 255, 0), -1)
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
            if int(ids) == 1:
                cen1 = center
                cen["cen1"]=cen1
            elif int(ids) == 2:
                cen2 = center
                cen["cen2"]=cen2
            elif int(ids) == 3:
                cen3 = center
                cen["cen3"]=cen3
            elif int(ids) == 4:
                cen4 = center
                cen["cen4"]=cen4           
    
    return frame,cen