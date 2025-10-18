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