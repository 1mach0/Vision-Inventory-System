"""
Purpose:
Unified configuration loader.

What it does:
Loads YAML/JSON files defining model paths, thresholds, camera IDs.
Converts them into strongly-typed dataclasses (DetectorConfig, OCRConfig).
Makes tuning easy without editing source code.

Used by:
yolo_detector.py, validate.py, ocr.py.
"""