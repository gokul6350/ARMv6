import cv2 as cv
from cv2 import aruco
import numpy as np
from ultralytics import YOLO
import math
from datetime import datetime

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

 

def detect_objects(frame,model):
    calib_data_path = "/home/gokul/Documents/Eye-arm/Cam calibarations/calib_data/MultiMatrix.npz"
    calib_data = np.load(calib_data_path)
    cam_mat = calib_data["camMatrix"]
    dist_coef = calib_data["distCoef"]


    Vconer = {'A':0, 'B':0}

    MARKER_SIZE = 2.7  # centimeters
    marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
    param_markers = aruco.DetectorParameters()

    classNames = ["ball", "battery", "grip"]

    def redist(corners1, corners2):
        rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(corners1, MARKER_SIZE, cam_mat, dist_coef)
        rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(corners2, MARKER_SIZE, cam_mat, dist_coef)

        tvec1 = tvec1.squeeze()
        tvec2 = tvec2.squeeze()

        distance = np.linalg.norm(tvec2 - tvec1)

        return distance

    def find_center(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        return center_x, center_y

    def draw_line_between_markers(frame, corners1, corners2):
        top_right1 = tuple(corners1[0].ravel().astype(int))
        top_right2 = tuple(corners2[0].ravel().astype(int))
        cv.line(frame, top_right1, top_right2, (0, 255, 0), 2)

    def detector(frame):
        cv.imshow("ORIGINAL",frame)
        results = model(frame)

        detected_objects = []
        object_coordinates = []
 
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
                    print(f"Battery found at coordinates (x1, y1): ({x1}, {y1}), (x2, y2): ({x2}, {y2})")
                    cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 3)
                    cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 1)
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    text = f"{class_name} ({confidence})"
                    cv.putText(frame, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                    detected_objects.append(class_name)
                    object_coordinates.append((battery_center[0], battery_center[1]))
     
        return {"objects": detected_objects, "coordinates": object_coordinates, "frame": frame}

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    result_dict = {"objects": [], "coordinates": [],"cen":[],"right":[]}
    centers = {}
    while len(centers) != 4:
        cv.imshow("OORIGINAL",frame)
        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_coef)
            centers = {}
            for i, (ids, corners) in enumerate(zip(marker_IDs, marker_corners)):
                cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
                center = tuple(map(int, np.mean(corners, axis=(1, 0))))
                cv.circle(frame, center, 5, (0, 255, 0), -1)
                cv.putText(frame, f"id: {ids[0]}", center, cv.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), 2)
                _corners = corners.reshape(4, 2)
                _corners = _corners.astype(int)
                top_right = _corners[0].ravel()
                
                if int(ids) == 1 or int(ids) == 2 or int(ids) == 3 or int(ids) == 4:
                    centers[int(ids)] = center
                    if int(ids) == 1:
                        coner1 = corners.reshape(1, 4, 2)
                        Vconer["A"]=tuple(top_right)
                        result_dict["right"]=tuple(top_right)
                    elif int(ids) == 2:
                        coner2 = corners.reshape(1, 4, 2)
                        Vconer["B"]=tuple(top_right)
                    elif int(ids) == 3:
                        coner3 = corners.reshape(1, 4, 2)
                    elif int(ids) == 4:
                        coner4 = corners.reshape(1, 4, 2)
            
            if len(centers) == 4:
                pt1 = tuple(map(int, centers[1]))
                pt2 = tuple(map(int, centers[2]))
                pt3 = tuple(map(int, centers[3]))
                pt4 = tuple(map(int, centers[4]))
                wi = round(redist(coner1, coner2), 1)
                le = round(redist(coner2, coner3), 1)
                
                print(f"real distance width {wi} length {le}")
                print(Vconer) 
                f_c=find_center(Vconer["A"],Vconer["B"])
                print(f">>><<<<{f_c}")                                                                                                                  
                pts_original = np.float32([pt1, pt2, pt4, pt3])  # Swap pt3 and pt4
                wii = wi * 10
                le = le * 10
                pts_transformed = np.float32([[0, 0], [wii, 0], [0, le], [wii, le]])
                matrix = cv.getPerspectiveTransform(pts_original, pts_transformed)
                result = cv.warpPerspective(frame, matrix, (int(wii), int(le)))
                result_frame = detector(result)
                cv.line(result, (int(13.5), int(13.5)), tuple(map(int, result_frame["coordinates"][0])), (0, 255, 10), 3)
                cv.imshow("Result",result)
                result_dict["objects"].extend(result_frame["objects"])
                result_dict["coordinates"].extend(result_frame["coordinates"])
                result_dict["cen"].extend(f_c)

            #,tuple(result_dict["right"])
#    cv.line(result,tuple(result_dict["coordinates"]),tuple(result_dict["cen"]),(0,255,10),3)
    cv.imwrite(f'logs/obj-{formatted_time}.jpg',result)
    return result_dict

