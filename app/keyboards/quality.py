"""Inline keyboards for video quality selection and download progress/cancellation."""

import hashlib
from typing import List, Optional
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_url_hash(url: str) -> str:
    """Generate a short 10-char hash for callback payload."""
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:10]


def get_quality_keyboard(
    available_qualities: List[int],
    url_hash: str,
    current_quality: Optional[int] = None,
    has_audio: bool = True,
) -> InlineKeyboardMarkup:
    """Generate inline keyboard with available video qualities and audio option.

    Only displays qualities that actually exist in available_qualities.

    Args:
        available_qualities: List of available heights (e.g. [1080, 720, 480, 360])
        url_hash: Short URL hash reference for callback routing
        current_quality: Currently selected/sent quality to mark with checkmark
        has_audio: Whether audio download option should be shown

    Returns:
        InlineKeyboardMarkup
    """
    rows: List[List[InlineKeyboardButton]] = []
    current_row: List[InlineKeyboardButton] = []

    # Sort qualities descending (e.g. 1080, 720, 480, 360)
    sorted_q = sorted(available_qualities, reverse=True)

    for q in sorted_q:
        label = f"✓ {q}p" if q == current_quality else f"📺 {q}p"
        if q == 720 and q != current_quality:
            label = "🎬 720p"

        btn = InlineKeyboardButton(
            text=label,
            callback_data=f"dl_q:{q}:{url_hash}",
        )
        current_row.append(btn)

        if len(current_row) == 2:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    if has_audio:
        rows.append(
            [
                InlineKeyboardButton(
                    text="🎵 Audio (MP3)",
                    callback_data=f"dl_audio:{url_hash}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_cancel_keyboard(job_id: str) -> InlineKeyboardMarkup:
    """Generate cancel button keyboard for in-progress download status message."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Cancel Download",
                    callback_data=f"cancel:{job_id}",
                )
            ]
        ]
    )
