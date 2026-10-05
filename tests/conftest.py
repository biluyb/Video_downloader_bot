"""Shared pytest fixtures."""

import os
import pytest


@pytest.fixture(autouse=True)
def _set_test_env(monkeypatch):
    """Ensure tests never use a real bot token."""
    monkeypatch.setenv("BOT_TOKEN", "test_token_12345")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TEMP_DIR", "/tmp/lookvidbot_test")
