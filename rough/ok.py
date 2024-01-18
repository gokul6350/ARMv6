import cv2 as cv
from cv2 import aruco
import numpy as np
from ultralytics import YOLO
import math
from datetime import datetime

calib_data_path = "/home/gokul/Documents/armv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
model=YOLO("best.pt")
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

classNames = ["ball", "battery", "grip"]
result_dict = {"detect_obj": [], "cen": [],"frame":[]}
vid = cv.VideoCapture(0)
def redist(corners1, corners2):
    rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(corners1, MARKER_SIZE, cam_mat, dist_coef)
    rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(corners2, MARKER_SIZE, cam_mat, dist_coef)

    tvec1 = tvec1.squeeze()
    tvec2 = tvec2.squeeze()

    distance = np.linalg.norm(tvec2 - tvec1)

    return distance

detected_objects = {}

def detector(frame):
    cv.imshow("ORIGINAL", frame)
    results = model(frame)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_name = classNames[int(box.cls[0])]

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

    return frame, detected_objects  # Return the frame and detected_objects

global centers 

def detect_marker(frame):
    centers = {}
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    rVec = None
    tVec = None
    coner1 = None
    coner2 = None
    coner3 = None

    if marker_corners:
        for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
            cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
            center = tuple(map(int, np.mean(corners, axis=(1, 0))))
            cv.circle(frame, center, 5, (0, 255, 0), -1)
            cv.putText(frame, f"id: {ids[0]}", center, cv.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), 2)

            if int(ids[0]) in range(1, 5):
                centers[int(ids[0])] = center


        if all(i in centers for i in [1, 2, 3]):
            # Corrected indexing using [0] to extract the array from the tuple
            coner1 = marker_corners[np.where(marker_IDs == 1)[0]].reshape(1, 4, 2)
            coner2 = marker_corners[np.where(marker_IDs == 2)[0]].reshape(1, 4, 2)
            coner3 = marker_corners[np.where(marker_IDs == 3)[0]].reshape(1, 4, 2)

            pt1 = tuple(map(int, centers[1]))
            pt2 = tuple(map(int, centers[2]))
            pt3 = tuple(map(int, centers[3]))

            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
            )

    else:
        print("Not found ARUCO codes")
        cv.imshow("free", frame)

    # return rVec, tVec, coner1, coner2, coner3
    return rVec, tVec, centers, frame

  
def detection():
    for x in range (4):
        ret,frame = vid.read()
        if not ret:
            print(f"not working")
            #break
        print(f"dwa   {ret}")
        cv.imwrite(f'logs3/gbomba(1)-{formatted_time}.jpg', frame)

        rvec,tvec,centers,frame=detect_marker(frame=frame)
        cv.imwrite(f'logs3/gbomba-maker(2)-{formatted_time}.jpg', frame)
        frame,object=detector(frame=frame)
        cv.imwrite(f'logs3/gbomba-detection(3)-{formatted_time}.jpg', frame)
        cv.imshow("sdads",frame)


detection()
