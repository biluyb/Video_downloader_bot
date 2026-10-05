"""/help command handler."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.main import get_help_keyboard
from app.utils.logger import get_logger

router = Router(name="help")
logger = get_logger(__name__)

HELP_TEXT = (
    "<b>How to use Download Via Link:</b>\n\n"
    "1️⃣ Copy a video link\n"
    "2️⃣ Send it here\n"
    "3️⃣ I'll automatically download it in 720p\n"
    "4️⃣ Choose another quality or audio if needed\n\n"
    "👥 <b>In groups:</b>\n"
    "Just send the link.\n"
    "No command is required.\n\n"
    "That's it! 🚀"
)

ABOUT_TEXT = (
    "<b>Download Via Link</b>  —  @lookvidbot\n\n"
    "🔗 Send a video link\n"
    "🎬 720p by default\n"
    "📺 1080p • 720p • 480p • 360p\n"
    "🎵 Audio download\n"
    "⚡ Fast & simple\n\n"
    "Download videos from YouTube, TikTok, Instagram, "
    "Facebook, X, Reddit, Vimeo, and many other "
    "supported platforms.\n\n"
    "version 0.1.0"
)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle the /help command."""
    logger.info("User %s requested help", message.from_user.id if message.from_user else "unknown")
    await message.answer(
        HELP_TEXT,
        reply_markup=get_help_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("about"))
async def cmd_about(message: Message) -> None:
    """Handle the /about command."""
    logger.info("User %s requested about", message.from_user.id if message.from_user else "unknown")
    await message.answer(
        ABOUT_TEXT,
        reply_markup=get_help_keyboard(),
        parse_mode="HTML",
    )
