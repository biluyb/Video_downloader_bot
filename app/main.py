"""Download Via Link — main entry point.

Starts the aiogram bot with long-polling.
"""

import asyncio
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config.settings import get_settings
from app.database.database import init_db
from app.handlers import (
    callbacks_router,
    download_router,
    help_router,
    history_router,
    start_router,
)
from app.utils.logger import get_logger, setup_logging


async def main() -> None:
    """Initialise and start the bot."""
    setup_logging()
    logger = get_logger(__name__)

    # Ensure static ffmpeg binaries are in PATH
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
    except Exception as fe:
        logger.warning("static_ffmpeg setup warning: %s", fe)

    settings = get_settings()

    # ── Validate token ────────────────────────────────────────
    if (
        not settings.bot_token
        or settings.bot_token == "replace_with_your_new_bot_token"
    ):
        logger.critical(
            "BOT_TOKEN is not configured.  "
            "Copy .env.example → .env and set your BotFather token."
        )
        sys.exit(1)

    # ── Ensure working directories exist ──────────────────────
    Path(settings.temp_dir).mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(parents=True, exist_ok=True)

    # ── Initialize Database ──────────────────────────────────
    try:
        await init_db()
    except Exception as dbe:
        logger.error("Failed to initialize database: %s", dbe)

    logger.info("Starting Download Via Link (@lookvidbot) v0.1.0")

    # ── Bot & dispatcher ──────────────────────────────────────
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Register routers in priority order
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(history_router)
    dp.include_router(callbacks_router)
    dp.include_router(download_router)  # Handles text URLs

    # ── Start polling ─────────────────────────────────────────
    logger.info("Bot is running. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
