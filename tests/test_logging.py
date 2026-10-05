"""Tests for the logging utility."""

import logging

from app.utils.logger import setup_logging, get_logger


class TestLogging:
    """Logging configuration tests."""

    def test_setup_logging_creates_handler(self):
        setup_logging()
        root = logging.getLogger()
        assert len(root.handlers) >= 1

    def test_get_logger_returns_named_logger(self):
        logger = get_logger("test.module")
        assert logger.name == "test.module"

    def test_aiogram_logger_is_warning(self):
        setup_logging()
        aiogram_logger = logging.getLogger("aiogram")
        assert aiogram_logger.level == logging.WARNING
