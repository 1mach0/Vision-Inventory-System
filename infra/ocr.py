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
import numpy as np
import pytesseract
import cv2
import regex as re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Union

try:
    from .config import CONFIG, OCRConfig
    OCR_CONFIG = CONFIG.ocr
    print("Successfully loaded OCR config from config.py")
except ImportError:
    print("config.py or CONFIG.ocr not found")

@dataclass
class OCRResult:
    raw_text: str
    confidence: Optional[float] = None
    parsed_fields: Dict[str, str] = field(default_factory=dict)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Use adaptive thresholding to enhance text
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return processed

def ocr_on_image(image_path):
    proccessed_img = preprocess_image(image_path)
    custom_config = f'-l {OCR_CONFIG.language} --oem 3 --psm 6' #Assume a single uniform block of text.
    data = pytesseract.image_to_data(proccessed_img, output_type=pytesseract.Output.DICT, config=custom_config)
    texts = []
    confidences = []
    for i, word in enumerate(data['text']):
        if float(data['conf'][i]) > 50 and word.strip():
            texts.append(word)
            confidences.append(float(data['conf'][i]))
    full_text = ' '.join(texts)
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    parsed = {}
    for key, pattern in OCR_CONFIG.regex_patterns.items():
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            if match.groups() :
                extracted_text = match.group(1).strip() 
            else : 
                extracted_text = match.group(0).strip()
            # The key is the name from the config (like 'serial' for example) and the value is the extracted_text.
            parsed[key] = extracted_text
                
    return OCRResult(raw_text=full_text, confidence=avg_confidence, parsed_fields=parsed)   

