"""
Purpose:
Central definition of “entities” in your system — like Detection, ValidationResult, Operator, and OCRResult.

What it does:
Defines @dataclass types for structured data passing.
Serves as the single source of truth for what a “detection” or “result” means.

Used by:
Every layer. Infra returns them, app manipulates them, frontend displays them.
"""