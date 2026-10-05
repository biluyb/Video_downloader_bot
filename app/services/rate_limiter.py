"""Rate limiting service for per-user and per-group limits."""

import time
from collections import defaultdict, deque
from typing import Dict, Deque, Tuple
import asyncio

from app.config.settings import get_settings


class RateLimiter:
    """In-memory rate limiter tracking active downloads and hourly request frequencies."""

    def __init__(self):
        self.settings = get_settings()

        # Active downloads counts
        self.active_user_downloads: Dict[int, int] = defaultdict(int)
        self.active_group_downloads: Dict[int, int] = defaultdict(int)

        # Timestamps of downloads in the last 3600 seconds
        self.user_history: Dict[int, Deque[float]] = defaultdict(deque)

        self._lock = asyncio.Lock()

    async def can_download(self, user_id: int, chat_id: int, is_group: bool) -> Tuple[bool, str]:
        """Check if user/group is permitted to start a new download.

        Args:
            user_id: Telegram User ID
            chat_id: Telegram Chat ID
            is_group: True if group or supergroup chat

        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        async with self._lock:
            now = time.time()
            cutoff = now - 3600

            # Clean old history
            user_timestamps = self.user_history[user_id]
            while user_timestamps and user_timestamps[0] < cutoff:
                user_timestamps.popleft()

            # Check hourly rate limit
            if len(user_timestamps) >= self.settings.max_downloads_per_hour:
                return False, f"Hourly download limit reached ({self.settings.max_downloads_per_hour}/hour). Please try again later."

            # Check active downloads for user
            if self.active_user_downloads[user_id] >= self.settings.max_concurrent_per_user:
                return False, "You already have a download in progress. Please wait for it to complete."

            # Check active downloads for group
            if is_group and self.active_group_downloads[chat_id] >= self.settings.max_concurrent_per_group:
                return False, "This group already has an active download in progress. Please wait for it to complete."

            return True, "Allowed."

    async def acquire(self, user_id: int, chat_id: int, is_group: bool) -> None:
        """Register the start of an active download."""
        async with self._lock:
            self.active_user_downloads[user_id] += 1
            if is_group:
                self.active_group_downloads[chat_id] += 1
            self.user_history[user_id].append(time.time())

    async def release(self, user_id: int, chat_id: int, is_group: bool) -> None:
        """Register completion/cancellation of an active download."""
        async with self._lock:
            if self.active_user_downloads[user_id] > 0:
                self.active_user_downloads[user_id] -= 1
            if is_group and self.active_group_downloads[chat_id] > 0:
                self.active_group_downloads[chat_id] -= 1


_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get singleton RateLimiter instance."""
    return _rate_limiter
