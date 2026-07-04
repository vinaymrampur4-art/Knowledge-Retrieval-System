"""
logger.py

Central logging configuration for the Knowledge Retrieval System.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import colorlog

from app.core.config import LOG_FILE, LOG_LEVEL


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.
    """

    logger = logging.getLogger("KRS")

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    # Ensure log directory exists
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # File Handler
    # -----------------------------
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(file_formatter)

    # -----------------------------
    # Console Handler
    # -----------------------------
    console_handler = colorlog.StreamHandler()

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler.setFormatter(console_formatter)

    # -----------------------------
    # Add Handlers
    # -----------------------------
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()