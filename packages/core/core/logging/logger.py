"""Small logger factory used across services.

This is intentionally tiny in phase 1. We can later upgrade it to structured
JSON logging without changing import paths throughout the codebase.
"""

import logging

from packages.core.core.config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Build or retrieve a configured logger instance."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)

