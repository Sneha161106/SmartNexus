from ultralytics import YOLO
import cv2

model = YOLO("models/yolov8s.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    frame = results[0].plot()

    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) == 27:
        break