"""
Purpose:
Standardizes logging across the entire CV module.

What it does:
Configures Python’s logging system (file + console output).
Ensures consistent format across all submodules.
Supports log rotation or alerting hooks.

Used by:
Every file in infra/, and optionally cv_module.py.
"""