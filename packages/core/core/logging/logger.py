"""Small logger factory used across services."""

from __future__ import annotations

import logging

from packages.core.core.config.settings import settings


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def _resolve_log_level() -> int:
    return getattr(logging, settings.log_level.upper(), logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Build or retrieve a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(_resolve_log_level())

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)

    logger.propagate = False
    return logger
