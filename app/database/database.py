"""Database connection and session management."""

from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.settings import get_settings
from app.database.models import Base
from app.utils.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()

# Ensure parent directory exists for SQLite
if "sqlite" in settings.database_url:
    db_file = settings.database_url.replace("sqlite+aiosqlite:///", "")
    Path(db_file).parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully.")
