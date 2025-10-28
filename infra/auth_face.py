"""
Purpose:
Lightweight local face verification for operator authentication.

What it does:
Uses DeepFace to generate embeddings.
Compares against saved embeddings in storage.py.
Returns True/False or match confidence.

Used by:
verify_operator.py.
"""

import numpy as np
from storage import load_faces
from typing import Tuple
from deepface import DeepFace

model_name = "VGG-Face"
detector_backend = "opencv"

confidence_threshold = 0.7

def get_embedding(frame_path) -> np.ndarray:
    result = DeepFace.represent(img_path=frame_path, model_name=model_name, detector_backend=detector_backend, max_faces=1)
    embedding = result[0]["embedding"]
    return embedding

def cosine_similarity(current_embedding, existing_embedding) -> float:
    dot_prod = np.dot(current_embedding, existing_embedding)
    norm_prod = np.linalg.norm(current_embedding) * np.linalg.norm(existing_embedding)
    return dot_prod / norm_prod

def verify_face(frame_path) -> Tuple[bool, str, float]:
    curr_embedding = get_embedding(frame_path)
    all_faces = load_faces()

    best_confidence = 0.0
    matched_name = ""

    for name, check_face_embedding in all_faces.items():
        check_embedding = np.array(check_face_embedding)
        confidence = cosine_similarity(curr_embedding, check_embedding)

        if confidence > best_confidence:
            best_confidence = confidence
            matched_name = name

    return best_confidence >= confidence_threshold, matched_name, best_confidence