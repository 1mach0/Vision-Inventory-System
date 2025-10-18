"""
construct the API bridge between our app and MIMS

Purpose:
Defines the CV_Module class, the entry point MIMS calls for all CV tasks.
This is the glue that ties everything together.

Responsibilities:
Initialize all infra components (camera, detector, OCR, etc.).
Expose clean methods like:
    validate_transaction(image, expected_item)
    verify_operator()
    scan_label()
Internally delegate work to the appropriate app/ use case.
Return clean ValidationResult or OCRResult objects to MIMS.

Used by:
__main__.py for standalone runs.
MIMS (imports CV_Module as a Python package).
"""


