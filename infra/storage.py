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