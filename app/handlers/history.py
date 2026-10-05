"""/history command handler showing recent downloads."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.database import AsyncSessionLocal
from app.database.repositories import Repository
from app.utils.logger import get_logger

router = Router(name="history")
logger = get_logger(__name__)


@router.message(Command("history"))
async def cmd_history(message: Message) -> None:
    """Handle /history command."""
    if not message.from_user:
        return

    user_id = message.from_user.id
    async with AsyncSessionLocal() as session:
        repo = Repository(session)
        records = await repo.get_user_history(user_id=user_id, limit=5)

    if not records:
        await message.answer("📜 <b>Recent Downloads</b>\n\nYou haven't downloaded any media yet!")
        return

    lines = ["📜 <b>Recent Downloads</b>\n"]
    for r in records:
        icon = "🎵" if r.quality == "audio" or r.format == "mp3" else "🎬"
        title = r.title or "Video"
        quality_str = r.quality or "720p"
        lines.append(f"{icon} <b>{title[:40]}</b> — <i>{quality_str}</i>")

    await message.answer("\n".join(lines), parse_mode="HTML")
