import cv2 as cv
from marker_detector import detect_markers
from object_detector import detector
from datetime import datetime
import numpy as np
from cv2 import aruco
MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()
calib_data_path = "/home/gokul/Documents/armv6/ARMv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
#global objs

def combine_dicts_overwrite(dict1, dict2):
    """Merges dictionaries, overwriting existing keys from the second dict.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict or list): The second dictionary or a list containing a dictionary.

    Returns:
        dict: The combined dictionary with overlapping keys overwritten.
    """
    if isinstance(dict2, list):
        if len(dict2) > 0:
            dict2 = dict2[0]  
        else:
            return dict1 
    return {key: value if key not in dict2 else dict2[key] for key, value in dict1.items()} | dict2

def prespective_transforme(frame,cen,cor):
    pts_original = np.float32([cen["cen1"],cen["cen2"],cen["cen4"],cen["cen3"]])
    wi = round(redist(cor["con1"], cor["con2"]), 1)
    le = round(redist(cor["con2"], cor["con3"]), 1)

    #NOT wi,le = wi*10 , le*10
    wi,le=28.7*10,35.7*10
    pts_transformed = np.float32([[0, 0], [wi, 0], [0, le], [wi, le]])
    matrix = cv.getPerspectiveTransform(pts_original, pts_transformed)
    result = cv.warpPerspective(frame, matrix, (int(wi), int(le)))
    origin=wi/2
    return result,wi/2
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
frea=np.zeros((608, 608, 3), dtype=np.uint8)
def cam():
    objs ={}
    global frea
    vid = cv.VideoCapture(0)
    while True:
        
    #def start_cam(vid):
        ret, frame = vid.read()
        if not ret:
            print("Error reading frame")
            exit()

        frame, cen, cor = detect_markers(frame)
        if frame.any():
            print("Frame is not None")
        else:
            print("Frame is a NoneType")
            exit()

        if cen["cen1"] == [] or cen["cen2"] == [] or cen["cen3"] == [] or cen["cen4"] == []:
            print("ValueError! Not enough center points")
            cv.imshow('Frame', frea)
        elif len(cen) == 4:
            frame11, origin = prespective_transforme(frame, cen, cor)
            cv.imshow('Frame', frame11)
            frea=frame11.copy()
          #  frame12,objs2 = detector(frame11)
          #  objs=combine_dicts_overwrite(objs,objs2)
           # print(f">>>{objs}")
       # print(i)
        if cv.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key press
            break
    
  
    vid.release()
    cv.destroyAllWindows()
            
    #start_cam(vid)        

  #  return objs,origin,frame12
cam()
print("VISION LOADED")