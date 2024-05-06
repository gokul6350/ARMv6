import cv2
from ultralytics import YOLO ,checks
import math

model = YOLO('best5.pt')

print(checks())


def locate(results,frame):
    detected_objects = {}
    classNames = [ "battery","glue", "lead","object_1"]
    for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                class_name = classNames[int(box.cls[0])]
                print(class_name)

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                center = (cx, cy)
                #cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 3)
                #cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 1)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                text = f"{class_name} ({confidence})"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                
                detected_objects.setdefault(class_name, []).append(center)
    return detected_objects

def detector(frame):
   
    


        
        results = model(frame)
        
        
        
        annotated_frame = results[0].plot()
        detected_objects=locate(results=results,frame=annotated_frame)

        #cv2.imshow("YOLOv8 Inference", annotated_frame)
        #print(detected_objects)

        return annotated_frame,detected_objects
      




