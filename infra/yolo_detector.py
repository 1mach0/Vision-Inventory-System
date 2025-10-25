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
import time
from pathlib import Path
from typing import Optional

class YOLODetector:
    def __init__(self, weights_path: str = "./../models/yolov8.pt"):
        self.weighs_path = Path(weights_path)
        if not self.weights_path.exists():
            raise FileNotFoundError(f"YOLO weights not found at {self.weights_path}")
        
        self.yolo_model = YOLO(str(self.weighs_path))

    def detect(self, frame, frame_id: Optional[int] = None):
        results = self.yolo_model(frame)
        detections = []

        ## time in milli-seconds
        timestamp = int(time.time() * 1000)

        for result in results:
            for box, class_id, confidence, in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                detections.append(Detection(id=int(class_id), label=CLASS_MAP.get(int(class_id), f"Class-{class_id}"), confidence=float(confidence), bbox=tuple(box.tolist()), timestamp=timestamp, frame_id=frame_id))

        return detections
    

# if __name__ == "__main__":
#     import cv2
#     detector = YOLODetector()
#     frame = cv2.imread("test_image.jpg")
#     detections = detector.detect(frame)
#     for det in detections:
#         print(det)



