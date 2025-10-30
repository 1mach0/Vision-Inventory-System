"""
Purpose:
Centralized persistence layer for logs, detections, and embeddings.

What it does:
Handles:
    Detection logs (who did what, when, and what was seen).
    Face database (authorized operators).
Can use SQLite, JSON, or CSV for prototype stage.
Provides APIs: save_detection(), load_faces(), reset_database().

Used by:
All app modules that need persistence.
"""

# Using JSON for simplicity
import json
from typing import Dict, List
from pathlib import Path

BASE_PATH = Path("./data") # this can be changed
FACES_FILE = BASE_PATH / "faces.json"
DETECTIONS_FILE = BASE_PATH / "detections.json"
BASE_PATH.mkdir(exist_ok=True)

def load_faces() -> Dict[str, List[float]]:
    if FACES_FILE.exists():
        with open(FACES_FILE, "r") as f:
            return json.loads(f)
        
    return {}

def save_face(name: str, embedding: List[float]):
    faces = load_faces()
    faces[name] = embedding

    with open(FACES_FILE, "w") as f:
        json.dump(faces, f)

def reset_faces():
    if FACES_FILE.exists():
        FACES_FILE.unlink()

def reset_detection():
    if DETECTIONS_FILE.exists():
        DETECTIONS_FILE.unlink()

def save_detection(log: Dict):
    logs = []
    if DETECTIONS_FILE.exists():
        with open(DETECTIONS_FILE, "r") as f:
            logs = json.load(f)
    logs.append(log)
    with open(DETECTIONS_FILE, "w") as f:
        json.dump(logs, f)


def reset_database():
    reset_detection()
    reset_faces()
    