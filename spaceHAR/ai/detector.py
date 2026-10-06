import cv2

from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    DETECTION_CONFIDENCE
)


class ObjectDetector:

    def __init__(self):

        print("Loading YOLO model...")

        self.model = YOLO(YOLO_MODEL)

        print("YOLO model loaded.")

    def detect(self, frame):

        if frame is None:
            return []

        results = self.model.predict(
            source=frame,
            conf=DETECTION_CONFIDENCE,
            verbose=False
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        names = result.names

        for box in result.boxes:

            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            width = max(1, x2 - x1)
            height = max(1, y2 - y1)

            area = width * height

            detections.append({
                "class_id": cls_id,
                "class_name": names.get(cls_id, str(cls_id)),
                "confidence": round(confidence, 3),
                "bbox": [x1, y1, x2, y2],
                "center": [center_x, center_y],
                "area": area
            })

        return detections

    def draw(self, frame, detections):

        if frame is None:
            return frame

        output = frame.copy()

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            label = (
                f'{detection["class_name"]} '
                f'{detection["confidence"]:.2f}'
            )

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                output,
                label,
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return output