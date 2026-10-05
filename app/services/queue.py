"""Asyncio Queue manager for global download concurrency control."""

import asyncio
from typing import Optional

from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DownloadQueueManager:
    """Manages global concurrency limits via asyncio Semaphore."""

    def __init__(self):
        self.settings = get_settings()
        self._semaphore: Optional[asyncio.Semaphore] = None

    @property
    def semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.settings.max_concurrent_downloads)
        return self._semaphore


_queue_manager = DownloadQueueManager()


def get_queue_manager() -> DownloadQueueManager:
    return _queue_manager
