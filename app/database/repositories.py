"""Data access repository for users and download history."""

from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import urlparse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import DownloadRecord, User
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Repository:
    """Repository handling CRUD operations for User and DownloadRecord models."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_user_id: int, username: Optional[str] = None) -> User:
        """Fetch or insert a user record, updating last_seen."""
        stmt = select(User).where(User.telegram_user_id == telegram_user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_user_id=telegram_user_id,
                username=username,
                first_seen=datetime.now(timezone.utc),
                last_seen=datetime.now(timezone.utc),
            )
            self.session.add(user)
        else:
            user.last_seen = datetime.now(timezone.utc)
            if username and user.username != username:
                user.username = username

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def log_download(
        self,
        user_id: int,
        chat_id: int,
        chat_type: str,
        url: str,
        title: Optional[str] = None,
        quality: Optional[str] = None,
        format_name: Optional[str] = None,
        file_size: Optional[int] = None,
        status: str = "completed",
    ) -> DownloadRecord:
        """Create a download history record."""
        domain = None
        try:
            domain = urlparse(url).netloc
        except Exception:
            pass

        record = DownloadRecord(
            user_id=user_id,
            chat_id=chat_id,
            chat_type=chat_type,
            url=url,
            domain=domain,
            title=title,
            quality=quality,
            format=format_name,
            file_size=file_size,
            status=status,
            created_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc) if status == "completed" else None,
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_user_history(self, user_id: int, limit: int = 10) -> List[DownloadRecord]:
        """Fetch recent downloads for a user."""
        stmt = (
            select(DownloadRecord)
            .where(DownloadRecord.user_id == user_id)
            .order_by(DownloadRecord.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
