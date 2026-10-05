"""Tests for handler text content and keyboard structure."""

import pytest

from app.handlers.start import START_TEXT
from app.handlers.help import HELP_TEXT, ABOUT_TEXT
from app.keyboards.main import get_start_keyboard, get_help_keyboard


class TestStartText:
    """Validate /start message content."""

    def test_contains_welcome(self):
        assert "Welcome" in START_TEXT

    def test_contains_720p(self):
        assert "720p" in START_TEXT

    def test_contains_audio(self):
        assert "Audio" in START_TEXT

    def test_contains_paste_instruction(self):
        assert "paste" in START_TEXT.lower() or "link" in START_TEXT.lower()


class TestHelpText:
    """Validate /help message content."""

    def test_contains_steps(self):
        assert "1️⃣" in HELP_TEXT
        assert "2️⃣" in HELP_TEXT
        assert "3️⃣" in HELP_TEXT
        assert "4️⃣" in HELP_TEXT

    def test_mentions_groups(self):
        assert "group" in HELP_TEXT.lower()

    def test_mentions_720p(self):
        assert "720p" in HELP_TEXT


class TestAboutText:
    """Validate /about message content."""

    def test_contains_bot_name(self):
        assert "Download Via Link" in ABOUT_TEXT

    def test_contains_username(self):
        assert "@lookvidbot" in ABOUT_TEXT

    def test_contains_platforms(self):
        for platform in ["YouTube", "TikTok", "Instagram", "Facebook"]:
            assert platform in ABOUT_TEXT

    def test_contains_version(self):
        assert "0.1.0" in ABOUT_TEXT


class TestKeyboards:
    """Validate keyboard structure."""

    def test_start_keyboard_has_help_and_about(self):
        kb = get_start_keyboard()
        buttons = [btn.text for row in kb.inline_keyboard for btn in row]
        assert "ℹ️ Help" in buttons
        assert "ℹ️ About" in buttons

    def test_start_keyboard_callback_data(self):
        kb = get_start_keyboard()
        callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        assert "help" in callbacks
        assert "about" in callbacks

    def test_help_keyboard_has_back(self):
        kb = get_help_keyboard()
        buttons = [btn.text for row in kb.inline_keyboard for btn in row]
        assert "🔙 Back" in buttons

    def test_help_keyboard_callback_data(self):
        kb = get_help_keyboard()
        callbacks = [btn.callback_data for row in kb.inline_keyboard for btn in row]
        assert "start" in callbacks
