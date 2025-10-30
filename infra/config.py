"""
Purpose:
Unified configuration loader.

What it does:
Loads YAML/JSON files defining model paths, thresholds, camera IDs.
Converts them into strongly-typed dataclasses (DetectorConfig, OCRConfig).
Makes tuning easy without editing source code.

Used by:
yolo_detector.py, validate.py, ocr.py.
"""
import yaml
from dataclasses import dataclass

@dataclass
class CameraConfig:
    index: int
    fps: int = 60

@dataclass
class StorageConfig:
    database_path: str

@dataclass
class AuthFaceConfig:
    model_name: str
    verification_threshold: float
    nms_threshold: float

@dataclass
class YoloDetectorConfig:
    model_path: str
    confidence_threshold: float

@dataclass
class OCRSystemConfig:
    engine: str
    min_confidence: float
    language: str = "eng"

@dataclass
class AppConfig:
    """Main configuration class that holds all component configs."""
    camera: CameraConfig
    storage: StorageConfig
    auth_face: AuthFaceConfig
    yolo_detector: YoloDetectorConfig
    ocr: OCRSystemConfig

def load_config(config_path: str = "config.yaml") -> AppConfig:
    """
    Loads the YAML configuration file and parses it into the AppConfig dataclass.
    """
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return AppConfig(
        camera=CameraConfig(**config_data['camera']),
        storage=StorageConfig(**config_data['storage']),
        auth_face=AuthFaceConfig(**config_data['auth_face']),
        yolo_detector=YoloDetectorConfig(**config_data['yolo_detector']),
        ocr=OCRSystemConfig(**config_data['ocr'])
    )

config = load_config()

# from infra.config import config
# config.auth_face.verification_threshold