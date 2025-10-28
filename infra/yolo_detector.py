"""
Purpose:
Encapsulates the object detection model (YOLOv8 or similar).

What it does:
Loads YOLOv8 weights from /models/.
Runs .detect(frame) and returns a list of Detection objects.
Uses class_map.py to translate numeric IDs into readable names.

Used by:
validate_transaction.py (and possibly scan_labels.py to locate label regions).
"""

from ..domain.models import Detection
from ultralytics import YOLO
from class_map import CLASS_MAP
from pathlib import Path
from typing import Optional
import time

class YOLODetector:
    def __init__(self, weights_path: str = Path(__file__).resolve().parent.parent / "models" / "yolov8.pt"):
        self.weights_path = Path(weights_path)
        if not self.weights_path.exists():
            raise FileNotFoundError(f"YOLO weights not found at {self.weights_path}")
        
        self.yolo_model = YOLO(str(self.weights_path))

    def detect(self, frame, frame_id: Optional[int] = None):
        results = self.yolo_model(frame)
        detections = []

        ## time in milliseconds
        timestamp = int(time.time() * 1000)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                detections.append(
                    Detection(
                        id=class_id,
                        label=CLASS_MAP.get(class_id, f"Class-{class_id}"),
                        confidence=confidence,
                        bbox=(x1, y1, x2, y2),
                        timestamp=timestamp,
                        frame_id=frame_id
                    )
                )

        return detections


# if __name__ == "__main__":
#     import cv2
#     detector = YOLODetector()
#     frame = cv2.imread("test_image.jpg")
#     detections = detector.detect(frame)
#     for det in detections:
#         print(det)



