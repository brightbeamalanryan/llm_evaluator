"""Logging configuration for eval-fw."""

from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

DEFAULT_LOG_FILE = "eval-fw.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEFAULT_BACKUP_COUNT = 24


def _has_handler(logger: logging.Logger, log_path: Path) -> bool:
    """Return True if a handler already writes to the given log path."""
    resolved = log_path.resolve()
    for handler in logger.handlers:
        if isinstance(handler, TimedRotatingFileHandler):
            handler_path = Path(handler.baseFilename).resolve()
            if handler_path == resolved:
                return True
    return False


def setup_logging(log_dir: Path, log_file: str = DEFAULT_LOG_FILE) -> Path:
    """Configure hourly rotating file logging and return the log path."""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_file

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not _has_handler(root_logger, log_path):
        handler = TimedRotatingFileHandler(
            log_path,
            when="H",
            interval=1,
            backupCount=DEFAULT_BACKUP_COUNT,
            encoding="utf-8",
            utc=True,

        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root_logger.addHandler(handler)

    return log_path
