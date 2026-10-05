"""/start command handler."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main import get_start_keyboard
from app.utils.logger import get_logger

router = Router(name="start")
logger = get_logger(__name__)

START_TEXT = (
    "👋 Welcome to <b>Download Via Link</b>!\n\n"
    "Send me a video link and I'll download it for you.\n\n"
    "🎬 720p by default\n"
    "📺 Other qualities available\n"
    "🎵 Audio download available\n\n"
    "Just paste your link below. 🚀"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle the /start command."""
    logger.info(
        "User %s (%s) started the bot",
        message.from_user.id if message.from_user else "unknown",
        message.from_user.username if message.from_user else "unknown",
    )
    await message.answer(
        START_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML",
    )
