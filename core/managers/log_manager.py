"""
===============================================================================
File        : log_manager.py
Project     : Video Frame Extractor

Description
-----------
Central logging manager for the application.

Features
--------
✓ Console logging
✓ File logging
✓ Thread-safe
✓ Timestamped messages
✓ Singleton friendly
✓ Easy to use

===============================================================================
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LogManager:
    """
    Central application logger.

    Example
    -------
    logger.info("Application started")
    logger.warning("Folder already exists")
    logger.error("Video could not be opened")
    """

    def __init__(
        self,
        log_file: Path | None = None,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
    ) -> None:

        if log_file is None:
            log_file = Path(__file__).resolve().parents[2] / "processing_log.txt"

        log_file.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("VideoFrameExtractor")

        # Prevent duplicate handlers if imported multiple times.
        if self._logger.handlers:
            return

        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Rotating File Handler
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)

    def exception(self, message: str) -> None:
        """
        Log an exception with traceback.
        Call this inside an except block.
        """
        self._logger.exception(message)