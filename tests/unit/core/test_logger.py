import logging

from packages.core.core.logging.logger import get_logger


def test_get_logger_reuses_handlers():
    logger = get_logger("openquant.tests.logger")
    handler_count = len(logger.handlers)

    logger2 = get_logger("openquant.tests.logger")

    assert logger2 is logger
    assert len(logger2.handlers) == handler_count
    assert logger2.propagate is False


def test_get_logger_uses_valid_level():
    logger = get_logger("openquant.tests.logger.level")

    assert logger.level in {
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    }
