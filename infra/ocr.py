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

try:
    from .config import CONFIG, OCRConfig
    OCR_CONFIG = CONFIG.ocr
    print("Successfully loaded OCR config from config.py")
except ImportError:
    print("Warning: iconfig.py or CONFIG.ocr not found")

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

def ocr_on_on_image(image):
    proccessed_img = preprocess_image(image)
    