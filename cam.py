
import object
import cv2 as cv 
from ultralytics import YOLO
def camera():

    print("Welcome to the Robot Arm Control System!")


    for _i in range(4):
        result = object.detect_objects()

        # Access objects and coordinates from the result dictionary
        detected_objects = result["detect_obj"]
     
        #right=(int(13.5), int(13.5))
        print(detected_objects)
        cen=result["cen"]
        key = cv.waitKey(1)
        if key == ord("q"):
            break
    

    return detected_objects,cen
  
        



    
