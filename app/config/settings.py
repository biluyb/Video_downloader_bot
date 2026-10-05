"""Application settings loaded from environment variables.

All configuration is loaded via pydantic-settings from environment
variables or a .env file.  The real BOT_TOKEN must NEVER be committed
to source control.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot configuration — every value is overridable via env vars."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Telegram ──────────────────────────────────────────────
    bot_token: str = "replace_with_your_new_bot_token"

    # ── Database ──────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"

    # ── Paths ─────────────────────────────────────────────────
    temp_dir: str = "./downloads"

    # ── Concurrency ───────────────────────────────────────────
    max_concurrent_downloads: int = 2
    max_concurrent_per_user: int = 1
    max_concurrent_per_group: int = 1

    # ── Queue ─────────────────────────────────────────────────
    max_queue_size: int = 20

    # ── Limits ────────────────────────────────────────────────
    max_file_size_mb: int = 500
    max_video_duration_minutes: int = 30

    # ── Rate limiting ─────────────────────────────────────────
    max_downloads_per_hour: int = 10

    # ── Timeout ───────────────────────────────────────────────
    download_timeout_seconds: int = 1800

    # ── Logging ───────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Derived helpers ───────────────────────────────────────
    @property
    def temp_path(self) -> Path:
        """Return *temp_dir* as a resolved ``Path``."""
        return Path(self.temp_dir).resolve()

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton ``Settings`` instance."""
    return Settings()
