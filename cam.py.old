
import object
import cv2 as cv 
from ultralytics import YOLO
def camera():

    print("Welcome to the Robot Arm Control System!")

    obj_found={}
    cap = cv.VideoCapture(0)
    model = YOLO("best.pt")
    for _i in range(4):
        ret, frame = cap.read()
        if not ret:
            break
        print(_i)
        result = object.detect_objects(frame,model)

        # Access objects and coordinates from the result dictionary
        detected_objects = result["objects"]
        object_coordinates = result["coordinates"]
        right=(int(13.5), int(13.5))
        print("Detected Objects and Coordinates:")
        for obj, coord in zip(detected_objects, object_coordinates):
            print("====================")
            obj_found[obj]=coord
            
            if obj == "battery":
                print(f"🔋battery:{coord}")
            else:
                print(f"{obj}: {coord}")

        cenn_ = result["cen"]
        key = cv.waitKey(1)
        if key == ord("q"):
            break
    print(obj_found,cenn_)
    cap.release()
    cv.destroyAllWindows()
    return obj_found,cenn_,right
  
        



    
