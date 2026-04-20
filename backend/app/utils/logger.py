from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings


_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def _configure_root_logger() -> None:
    if logging.getLogger().handlers:
        return

    Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(_LOG_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(settings.log_file, maxBytes=5_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO), handlers=[stream_handler, file_handler])


def get_logger(name: str) -> logging.Logger:
    _configure_root_logger()
    return logging.getLogger(name)
