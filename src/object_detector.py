import cv2 as cv
from ultralytics import YOLO
import math

model = YOLO("best.pt")
classNames = ["ball", "battery", "grip"]

def detector(frame):
    results = model(frame, stream=True)
    detected_objects = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_name = classNames[int(box.cls[0])]
            print(class_name)

            if class_name == "battery":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                battery_center = (cx, cy)
                cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 3)
                cv.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 1)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                text = f"{class_name} ({confidence})"
                cv.putText(frame, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                detected_objects.append({class_name:battery_center})
    print(f"<><><>{detected_objects}")
    return frame, detected_objects