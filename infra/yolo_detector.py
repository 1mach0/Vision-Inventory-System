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