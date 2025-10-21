"""
Purpose:
Central definition of “entities” in your system — like Detection, ValidationResult, Operator, Inventory Item and OCRResult.

YOLO detector returns → Detection
OCR returns → OCRResult
Transaction validator returns → ValidationResult
User authentication returns → Operator

What it does:
Defines @dataclass types for structured data passing.
Serves as the single source of truth for what a “detection” or “result” means.

Used by:
Every layer. Infra returns them, app manipulates them, frontend displays them.
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class Detection:
    id: int
    label: str
    confidence: float
    bbox: tuple[float, float, float, float]
    timestamp: int
    frame_id: Optional[int]=None # which frame it came from

@dataclass
class OCRResult:
    text: str
    confidence: float
    bbox: tuple[float, float, float, float]
    source_id: Optional[int]=None

@dataclass
class ValidationResult:
    success: bool
    message: str
    timestamp: float
    operator_id: Optional[int]=None
    related_items: Optional[list[str]]=None


@dataclass
class Operator:
    id: int
    name: str
    face_embedding: np.ndarray
    access_level: str
    last_login: Optional[float]=None

@dataclass
class InventoryItem:
    id: int
    name: str
    quantity: str
    location: Optional[int]=None
    last_seen: Optional[float]=None