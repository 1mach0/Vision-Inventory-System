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

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("./../logs")
LOG_FILE = LOG_DIR / f"cv_module_{datetime.now():%Y-%m-%d}.log"

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] — %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MAX_SIZE_OF_FILE = 5 * 1024 * 1024 # 5MB file is set as max file size

os.makedirs(LOG_DIR, exist_ok=True)

def configure_logging(level=logging.INFO):
    if logging.getLogger().hasHandlers():
        # its already config-ed, avoids duplicate handlers
        return

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes = MAX_SIZE_OF_FILE,
        backupCount = 5 # keep 5 files until it deletes the oldest
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
