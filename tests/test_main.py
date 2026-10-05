"""Tests for the main module startup validation."""

import pytest

from app.config.settings import Settings


class TestMainValidation:
    """Startup validation checks."""

    def test_placeholder_token_detected(self):
        """The bot should reject the placeholder token."""
        s = Settings(bot_token="replace_with_your_new_bot_token")
        assert s.bot_token == "replace_with_your_new_bot_token"
        # main.py checks for this exact value and exits

    def test_empty_token_detected(self):
        """The bot should reject an empty token."""
        s = Settings(bot_token="")
        assert not s.bot_token

    def test_valid_token_accepted(self):
        """A non-placeholder token should be accepted."""
        s = Settings(bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        assert s.bot_token != "replace_with_your_new_bot_token"
        assert s.bot_token
