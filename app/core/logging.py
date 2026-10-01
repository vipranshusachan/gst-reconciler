"""Structured logging for GST Reconciler with privacy protection."""

import logging
import os
import re
import sys
from pathlib import Path

# Masking patterns to protect sensitive taxpayer data in logs
GSTIN_REGEX = re.compile(r"\b([0-9]{2})[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b")

class PrivacyFilter(logging.Filter):
    """Filters log records to mask full GSTINs and sensitive taxpayer identifiers."""
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = GSTIN_REGEX.sub(r"\g<1>**********", record.msg)
        return True


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(os.getenv("GST_RECONCILER_LOG_LEVEL", "INFO").upper())
        logger.addFilter(PrivacyFilter())

        # Console Handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        # File Handler in user AppData or local logs
        log_dir = Path.home() / ".gst_reconciler" / "logs"
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            f_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
            f_handler.setFormatter(c_format)
            logger.addHandler(f_handler)
        except OSError:
            pass  # Fall back to console only if directory unwritable

    return logger
