import cv2 as cv
from cv2 import aruco
import numpy as np


marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)


param_markers = aruco.DetectorParameters()


cap = cv.VideoCapture(0)
detector = cv.aruco.ArucoDetector(marker_dict, param_markers)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
  
    frame_height, frame_width = frame.shape[:2]
    

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    marker_corners, marker_IDs, reject = detector.detectMarkers(
        gray_frame
    )
    

    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
       
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
         
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            
         
            center = tuple(map(int, np.mean(corners, axis=0)))
            
   
            cv.putText(
                frame,
                f"id: {ids[0]}",
                (center[0] - 30, center[1] - 10),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
            

            for i in range(len(marker_IDs)):
                if i != ids[0]: 
                    next_corners = marker_corners[i][0]
                    next_center = tuple(map(int, np.mean(next_corners, axis=0)))
                    cv.line(frame, center, next_center, (0, 255, 0), 2)
    

    cv.line(frame, (0, 0), (frame_width, frame_height), (0, 165, 255), 1)
    cv.line(frame, (0, frame_height), (frame_width, 0), (0, 165, 255), 1)
    

    cv.imshow("frame", frame)
    
  
    key = cv.waitKey(1)
    if key == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
