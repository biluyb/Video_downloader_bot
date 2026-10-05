"""Tests for downloader job, progress tracking, and rate limiting."""

import pytest
from app.services.downloader import DownloadJob, DownloadProgress
from app.services.rate_limiter import RateLimiter


class TestDownloader:
    def test_job_initialization(self, monkeypatch):
        monkeypatch.setenv("BOT_TOKEN", "test_123")
        job = DownloadJob(url="https://youtube.com/watch?v=12345", target_quality=720)
        assert job.url == "https://youtube.com/watch?v=12345"
        assert job.target_quality == 720
        assert job.is_audio is False
        assert job.job_id.startswith("job_")
        assert job.cancelled is False

    def test_job_cancellation(self, monkeypatch):
        monkeypatch.setenv("BOT_TOKEN", "test_123")
        job = DownloadJob(url="https://youtube.com/watch?v=12345")
        job.cancel()
        assert job.cancelled is True
        assert job.progress.status == "cancelled"

    def test_progress_formatting(self):
        p = DownloadProgress(speed_bytes_per_sec=2 * 1024 * 1024, eta_seconds=75)
        assert p.formatted_speed == "2.0 MB/s"
        assert p.formatted_eta == "01:15"


class TestRateLimiter:
    @pytest.mark.asyncio
    async def test_rate_limiter_concurrency(self):
        limiter = RateLimiter()
        user_id = 12345
        chat_id = 99999

        allowed, _ = await limiter.can_download(user_id, chat_id, is_group=False)
        assert allowed is True

        await limiter.acquire(user_id, chat_id, is_group=False)
        allowed, reason = await limiter.can_download(user_id, chat_id, is_group=False)
        assert allowed is False
        assert "already have a download" in reason

        await limiter.release(user_id, chat_id, is_group=False)
        allowed, _ = await limiter.can_download(user_id, chat_id, is_group=False)
        assert allowed is True
