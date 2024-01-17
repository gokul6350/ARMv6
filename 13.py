import cv2 as cv
from cv2 import aruco
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import marker

calib_data_path = "/home/gokul/Documents/armv6/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
model = YOLO("best.pt")
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

MARKER_SIZE = 2.7
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
param_markers = aruco.DetectorParameters()

classNames = ["ball", "battery", "grip"]
result_dict = {"detect_obj": [], "cen": [], "frame": []}
vid = cv.VideoCapture(0)


def redist(corners1, corners2):
    rvec1, tvec1, _ = aruco.estimatePoseSingleMarkers(corners1, MARKER_SIZE, cam_mat, dist_coef)
    rvec2, tvec2, _ = aruco.estimatePoseSingleMarkers(corners2, MARKER_SIZE, cam_mat, dist_coef)

    tvec1 = tvec1.squeeze()
    tvec2 = tvec2.squeeze()

    distance = np.linalg.norm(tvec2 - tvec1)

    return distance

def prespective_transforme(frame,cen):
    pts_original = np.float32([cen["cen1"],cen["cen2"],cen["cen3"],cen["cen4"]])
    wi = round(redist(cen["cen1"], cen["cen2"]), 1)
    le = round(redist(cen["cen2"], cen["cen3"]), 1)

    wi,le = wi*10 , le*10
    pts_transformed = np.float32([[0, 0], [wi, 0], [0, le], [wi, le]])
    mat 
def main():
    while True:
        ret, frame = vid.read()
        if not ret:
            print("Error reading frame")
            break

        frame, cen = marker.detect_markers(frame)
        cv.imshow('frame', frame)

        if  cen["cen1"] == [] or cen["cen2"] == [] or cen["cen3"] == [] or cen["cen4"] == []:
            print("ValueError")
        elif len(cen) == 4:
            prespective_transforme(frame,cen)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv.destroyAllWindows()


main()
