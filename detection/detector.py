from ultralytics import YOLO

class Detector:

    def __init__(self):

        self.model = YOLO("models/yolov8s.pt")

    def detect(self, frame):

        objects = []

        results = self.model(frame, conf=0.5)

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])
                label = self.model.names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                objects.append((label, x1, y1, x2, y2))

        return objects