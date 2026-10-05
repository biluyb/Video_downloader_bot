"""Inline callback-query handlers.

Handles button presses from inline keyboards (help, about, back).
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery

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
