"""Tests for database models and repository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base
from app.database.repositories import Repository


@pytest.fixture
async def async_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_or_create_user(async_session):
    repo = Repository(async_session)
    user = await repo.get_or_create_user(telegram_user_id=1001, username="testuser")
    assert user.telegram_user_id == 1001
    assert user.username == "testuser"

    # Fetch again
    user2 = await repo.get_or_create_user(telegram_user_id=1001, username="updateduser")
    assert user2.id == user.id
    assert user2.username == "updateduser"


@pytest.mark.asyncio
async def test_log_and_get_history(async_session):
    repo = Repository(async_session)
    record = await repo.log_download(
        user_id=1001,
        chat_id=2002,
        chat_type="private",
        url="https://youtube.com/watch?v=xyz",
        title="Test Video",
        quality="720p",
        format_name="mp4",
        file_size=1048576,
        status="completed",
    )
    assert record.id is not None
    assert record.user_id == 1001
    assert record.domain == "youtube.com"

    history = await repo.get_user_history(user_id=1001, limit=5)
    assert len(history) == 1
    assert history[0].title == "Test Video"
