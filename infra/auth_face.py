"""
Purpose:
Lightweight local face verification for operator authentication.

What it does:
Uses InsightFace or similar model to generate embeddings.
Compares against saved embeddings in storage.py.
Returns True/False or match confidence.

Used by:
verify_operator.py.
"""

import numpy as np
from storage import load_faces
from typing import Tuple
from insightface.app import FaceAnalysis


## Ideally should be stored in config.py
THRESHOLD = 0.6         ## Verification threshold
NMS_THRESHOLD = 0.4     ## Non-Maximum Suppression threshold for face detection


app = FaceAnalysis(name='antelopev2')    ## lightweight face detection + embedding model
app.prepare(ctx_id=0, nms=NMS_THRESHOLD) 

def get_embedding(frame) -> np.ndarray:
    """
        Input: Takes a frame
        Output: Returns the embedding of the first face detected (Can be extended to all of them)
    """
    faces = app.get(frame)
    if not faces:
        return None
    return faces[0].embedding

def cosing_similarity(current_embedding, existing_embedding):
    return np.dot(current_embedding, existing_embedding) / (np.linalg.norm(current_embedding) * np.linalg.norm(existing_embedding))

def verify_face(frame) -> Tuple[bool, str, float]:
    """
        Compares detected face against stored embeddings.
        Returns: (is_verified, matched_name, confidence)
    """

    embedding = get_embedding(frame)
    if embedding is None:
        return False, None, 0.0
    
    all_faces = load_faces()
    max_conf = 0.0
    matched_name = None

    for name, face_embedding in all_faces.items():
        face_embedding = np.array(face_embedding) 
        conf = cosing_similarity(current_embedding=embedding, existing_embedding=face_embedding)

        if conf > max_conf:
            max_conf = conf
            matched_name = name
        
    return (max_conf >= THRESHOLD, matched_name, max_conf)