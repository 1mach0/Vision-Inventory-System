"""
Purpose:
Provides a hardware-agnostic way to access camera frames.

What it does:
Wraps OpenCV’s VideoCapture.
Handles .start_video(), .stop_video(), .get_frame().
Handles resizing, error catching, and thread safety if needed.

Used by:
All app use-cases needing live images (validation, label scanning, face verification).
"""