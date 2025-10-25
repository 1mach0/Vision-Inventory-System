"""
Purpose:
Maps YOLO’s numeric class IDs to human-readable labels.

What it does:
CLASS_MAP = {
    0: "Weapon-M4",
    1: "Medical-Kit",
    2: "Crate-Ammo"
}
Keeps your detection model clean and readable.
Optional: load from a YAML file for easy updates.

Used by:
yolo_detector.py.
"""

CLASS_MAP = {
    0: "Weapon-M4",
    1: "Medical-Kit",
    2: "Crate-Ammo"
}


