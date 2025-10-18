"""
Purpose:
Extract text from images (for serials, batch numbers, expiry).

What it does:
Uses Tesseract or OpenCV preprocessing to extract readable text.
Outputs structured OCRResult (text + confidence).
May include regex parsing for known label formats.

Used by:
scan_labels.py.
"""