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

import pytesseract as pytes
import cv2
from typing import Optional, Dict, List
import re

from domain.models import OCRResult
from infra.config import config
from infra.logger import get_logger

logger = get_logger(__name__)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    threshold = cv2.adaptiveThreshold(
        src=blur, # input grayscale image after smoothing
        maxValue=255, # white
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # gaussian weighted sum of neighbouring pixel vals
        thresholdType=cv2.THRESH_BINARY, # pixels above become white, pixels become black
        blockSize=31, # size of neighbourhood
        C=2 # constant subtracter from the mean
    )

    return threshold

def parse_fields(text: str) -> Dict[str, str]:
    fields = {}

    batch_match = re.search(r"Batch\s*(?:No\.?|Number)?[:\-]?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    exp_match = re.search(r"Exp(?:iry|\.|Date)?[:\-]?\s*([0-9/.-]{4,10})", text, re.IGNORECASE)
    serial_match = re.search(r"Serial\s*(?:No\.?)?[:\-]?\s*([A-Z0-9]+)", text, re.IGNORECASE)

    if batch_match:
        fields["batch"] = batch_match.group(1)
    if exp_match:
        fields["expiry"] = exp_match.group(1)
    if serial_match:
        fields["serial"] = serial_match.group(1)

    return fields

def extract_with_tesseract(image, lang="eng", source_id: Optional[int] = None) -> List[OCRResult]:
    preprocessed = preprocess_image(image)

    config_str = f"--psm 6 -l {lang} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:/.-"
    data = pytes.image_to_data(
        preprocessed,
        config=config_str,
        output_type=pytes.Output.DICT
    )

    results: List[OCRResult] = []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if not text:
            continue

        try:
            conf = float(data["conf"][i])
        except ValueError:
            conf = 0.0

        if conf < config.ocr.min_confidence:
            continue

        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        bbox = (x, y, x + w, y + h)

        parsed = parse_fields(text)

        result = OCRResult(
            text = text,
            confidence = conf,
            bbox = bbox,
            source_id = source_id,
            fields = parsed if parsed else None
        )

        results.append(result)

    logger.info(f"Tesseract OCR extracted {len(results)} text segments.")

    return results


# public functions

def extract_text(image, engine: Optional[str] = None) -> List[OCRResult]:
    if image is None:
        raise ValueError("No image provided for OCR extraction.")

    engine = engine or config.ocr.engine
    min_conf = config.ocr.min_confidence
    lang = config.ocr.language

    logger.info(f"OCR engine: {engine}, min_conf={min_conf}, lang={lang}")

    if engine == "tesseract":
        results = extract_with_tesseract(image, lang=lang)
    # elif engine == "paddle":
    #     results = extract_with_paddle(image, lang=lang)
    # elif engine == "easyocr":
    #     results = extract_with_easyocr(image, lang=lang)
    else:
        raise ValueError(f"Unknown OCR engine: {engine}")

    filtered = [r for r in results if r.confidence >= min_conf]
    logger.info(f"{len(filtered)} OCR results passed the confidence threshold ({min_conf})")

    return filtered

