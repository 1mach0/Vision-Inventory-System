"""
Purpose:
Implements logic to compare what the camera sees vs. what MIMS expects.

What it does:
Takes detections and an expected_item as input.
Returns a ValidationResult with match/mismatch info.
Can include thresholds (confidence cutoff, fuzzy string matching).

Used by:
validate_transaction.py.
"""

import time
from ..domain.models import ValidationResult
from typing import Optional
from logger import get_logger

logger = get_logger(__name__)

class Validator:
    def __init__(self):
        logger.info(f"Validator initialized")
        
    def validate(self, detections, expected_item: str, operator_id: Optional[int] = None) -> ValidationResult:
        logger.debug(f"Starting validation for operator_id={operator_id} with expected_item='{expected_item}'")
        detected_labels = [d.label for d in detections]
        logger.debug(f"Detected labels (after thresholding): {detected_labels}")
        
        if expected_item in detected_labels:
            message = f"Match found: {expected_item}"
            success = True
            logger.info(f"Validation success — {message}")
        else:
            message = f"Mismatch: Expected '{expected_item}', found {detected_labels or 'none'}"
            success = False
            logger.warning(f"Validation failed — {message}")

        timestamp = time.time()
        result = ValidationResult(success, message, timestamp, operator_id, related_items=detected_labels)
        logger.debug(f"ValidationResult created: {result}")
        return result

### example usage
# from camera_adapter import CameraAdapter
# from yolo_detector import YOLODetector

# camera = CameraAdapter()
# yolo_detector = YOLODetector()
# validator = Validator()

# frame = camera.get_frame()
# detections = yolo_detector.detect(frame)
# result = validator.validate(detections, expected_item="Bottle")

# print(result.message)
