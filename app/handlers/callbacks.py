"""Inline callback-query handlers for quality selection, audio download, and cancellation."""

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.handlers.download import active_jobs, process_media_download, url_hash_cache
from app.handlers.help import ABOUT_TEXT, HELP_TEXT
from app.handlers.start import START_TEXT
from app.keyboards.main import get_help_keyboard, get_start_keyboard
from app.utils.logger import get_logger

router = Router(name="callbacks")
logger = get_logger(__name__)


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery) -> None:
    """Show help via inline button."""
    logger.info("Callback: help from user %s", callback.from_user.id)
    await callback.message.edit_text(
        HELP_TEXT,
        reply_markup=get_help_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery) -> None:
    """Show about via inline button."""
    logger.info("Callback: about from user %s", callback.from_user.id)
    await callback.message.edit_text(
        ABOUT_TEXT,
        reply_markup=get_help_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "start")
async def cb_start(callback: CallbackQuery) -> None:
    """Navigate back to start screen."""
    logger.info("Callback: start from user %s", callback.from_user.id)
    await callback.message.edit_text(
        START_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel:"))
async def cb_cancel_download(callback: CallbackQuery) -> None:
    """Cancel an active in-progress download job."""
    job_id = callback.data.split(":")[1]
    job = active_jobs.get(job_id)
    if job:
        job.cancel()
        logger.info("User %s cancelled job %s", callback.from_user.id, job_id)
        await callback.answer("Cancelling download...")
    else:
        await callback.answer("Download already completed or expired.", show_alert=True)


@router.callback_query(F.data.startswith("dl_q:"))
async def cb_quality_download(callback: CallbackQuery) -> None:
    """Handle request for specific quality (1080p, 720p, 480p, 360p, etc.)."""
    parts = callback.data.split(":")
    quality = int(parts[1])
    u_hash = parts[2]

    url = url_hash_cache.get(u_hash)
    if not url:
        await callback.answer("Link reference expired. Please send the link again.", show_alert=True)
        return

    await callback.answer(f"Downloading {quality}p...")
    await process_media_download(
        message=callback.message,
        url=url,
        target_quality=quality,
        is_audio=False,
    )


@router.callback_query(F.data.startswith("dl_audio:"))
async def cb_audio_download(callback: CallbackQuery) -> None:
    """Handle request for MP3 audio download."""
    parts = callback.data.split(":")
    u_hash = parts[1]

    url = url_hash_cache.get(u_hash)
    if not url:
        await callback.answer("Link reference expired. Please send the link again.", show_alert=True)
        return

    await callback.answer("Preparing audio download...")
    await process_media_download(
        message=callback.message,
        url=url,
        target_quality=720,
        is_audio=True,
    )
