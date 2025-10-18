"""
Purpose:
Handle identity verification (face recognition) for high-security transactions.

What it does:
Capture operator image (camera_adapter).
Run simplified face recognition (infra.auth_face).
Compare against locally stored face embeddings (infra.storage).
Return True/False verification status.

Used by:
CV_Module.verify_operator(); MIMS calls it before allowing sensitive actions (e.g., weapon issue).
"""
