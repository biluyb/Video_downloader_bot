"""Main keyboard layouts used across the bot."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown with the /start greeting."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ℹ️ Help",
                    callback_data="help",
                ),
                InlineKeyboardButton(
                    text="ℹ️ About",
                    callback_data="about",
                ),
            ],
        ]
    )


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Keyboard shown after the help text."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="start",
                ),
            ],
        ]
    )
