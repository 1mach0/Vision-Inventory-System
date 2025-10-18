"""
Purpose:
Automate serial number / batch / expiry extraction from item labels.

What it does:
Capture image of item or label.
Preprocess (crop or zoom into label region).
Run OCR (infra.ocr).
Return parsed text fields (domain.models.OCRResult).
Optionally log extracted info to the database.

Used by:
CV_Module.scan_label(); called during stock entry/update when the user scans a physical item.
"""
