"""Tests for app.config.settings."""

import os
import pytest

from app.config.settings import Settings


class TestSettings:
    """Settings loading and validation."""

    def test_default_values(self):
        """Settings should have sensible defaults."""
        s = Settings(bot_token="test_123")
        assert s.max_concurrent_downloads == 2
        assert s.max_concurrent_per_user == 1
        assert s.max_concurrent_per_group == 1
        assert s.max_queue_size == 20
        assert s.max_file_size_mb == 500
        assert s.max_video_duration_minutes == 30
        assert s.max_downloads_per_hour == 10
        assert s.download_timeout_seconds == 1800
        # LOG_LEVEL is overridden to DEBUG by conftest for testing
        assert s.log_level in ("INFO", "DEBUG")

    def test_temp_path_property(self):
        """temp_path should return a resolved Path."""
        s = Settings(bot_token="test_123", temp_dir="./downloads")
        assert s.temp_path.is_absolute()
        assert str(s.temp_path).endswith("downloads")

    def test_max_file_size_bytes(self):
        """max_file_size_bytes should equal MB * 1024 * 1024."""
        s = Settings(bot_token="test_123", max_file_size_mb=100)
        assert s.max_file_size_bytes == 100 * 1024 * 1024

    def test_token_from_env(self, monkeypatch):
        """BOT_TOKEN should be loadable from environment."""
        monkeypatch.setenv("BOT_TOKEN", "env_token_xyz")
        s = Settings()
        assert s.bot_token == "env_token_xyz"

    def test_database_url_default(self):
        """Default database URL should use SQLite."""
        s = Settings(bot_token="test_123")
        assert "sqlite" in s.database_url
