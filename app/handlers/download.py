"""Download handler — automatically handles video URLs sent in private and group chats."""

import asyncio
import time
from pathlib import Path
from typing import Dict, Optional

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import FSInputFile, Message

from app.database.database import AsyncSessionLocal
from app.database.repositories import Repository
from app.keyboards.quality import get_cancel_keyboard, get_quality_keyboard, get_url_hash
from app.services.cleanup import cleanup_job_directory
from app.services.downloader import DownloadJob, DownloadProgress
from app.services.metadata import MediaMetadata, extract_metadata
from app.services.queue import get_queue_manager
from app.services.rate_limiter import get_rate_limiter
from app.utils.logger import get_logger
from app.utils.url_extractor import find_first_url
from app.utils.validators import validate_download_url

router = Router(name="download")
logger = get_logger(__name__)

# Active jobs map for cancellation
active_jobs: Dict[str, DownloadJob] = {}

# URL cache for hash lookup
url_hash_cache: Dict[str, str] = {}


def render_progress_bar(percent: float) -> str:
    """Render a 10-character progress bar."""
    filled = int(round(percent / 10))
    filled = max(0, min(10, filled))
    return "█" * filled + "░" * (10 - filled)


async def process_media_download(
    message: Message,
    url: str,
    target_quality: int = 720,
    is_audio: bool = False,
) -> None:
    """Main downloading flow for a given URL, user, and target quality."""
    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    is_group = message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)

    # 1. Rate Limiting Check
    rate_limiter = get_rate_limiter()
    allowed, reason = await rate_limiter.can_download(user_id, chat_id, is_group)
    if not allowed:
        await message.reply(f"⚠️ {reason}")
        return

    # 2. Initial status message
    status_msg = await message.reply("🔎 Analyzing link...")

    # Cache URL hash
    u_hash = get_url_hash(url)
    url_hash_cache[u_hash] = url

    # 3. Extract Metadata
    try:
        metadata: MediaMetadata = await extract_metadata(url)
    except Exception as e:
        logger.error("Metadata extraction failed for %s: %s", url, e)
        await status_msg.edit_text(
            "❌ Download failed.\n\n"
            "The link may be unsupported, unavailable, private, or temporarily inaccessible.\n\n"
            "Please try another link."
        )
        return

    # 4. Handle 720p availability & fallback
    if not is_audio:
        if target_quality == 720 and not metadata.is_720_available:
            actual_quality = metadata.best_quality_720
            await status_msg.edit_text(
                f"ℹ️ 720p isn't available.\n"
                f"Downloading the best available quality: <b>{actual_quality}p</b>...",
                parse_mode="HTML",
            )
            await asyncio.sleep(1.5)
            target_quality = actual_quality

    # 5. Acquire Concurrency Queue & Rate Limiter
    queue_manager = get_queue_manager()
    await rate_limiter.acquire(user_id, chat_id, is_group)

    job = DownloadJob(url=url, target_quality=target_quality, is_audio=is_audio)
    active_jobs[job.job_id] = job

    # Progress throttling state
    last_update_time = [0.0]

    def on_progress(prog: DownloadProgress) -> None:
        now = time.time()
        # Throttle progress updates to every 2.5 seconds
        if now - last_update_time[0] < 2.5 and prog.percent < 100.0:
            return

        last_update_time[0] = now
        bar = render_progress_bar(prog.percent)
        label = "🎵 Preparing audio..." if is_audio else f"⬇️ Downloading {target_quality}p..."

        text = (
            f"<b>{label}</b>\n\n"
            f"<code>{bar} {prog.percent:.0f}%</code>\n\n"
            f"{prog.percent:.0f}% • {prog.formatted_speed}\n"
            f"ETA: {prog.formatted_eta}"
        )
        # Schedule message edit without blocking worker thread
        asyncio.create_task(
            _safe_edit_message(status_msg, text, get_cancel_keyboard(job.job_id))
        )

    output_path: Optional[Path] = None

    try:
        async with queue_manager.semaphore:
            output_path = await job.run(callback=on_progress)

        if job.cancelled:
            await status_msg.edit_text("❌ Download cancelled.")
            return

        # 6. Uploading state message
        await status_msg.edit_text("📤 Uploading to Telegram...")

        # Prepare caption
        if is_audio:
            caption = f"🎵 <b>{metadata.title}</b>"
        else:
            caption = (
                f"🎬 <b>{metadata.title}</b>\n"
                f"⏱ Duration: {metadata.formatted_duration}\n"
                f"📺 Quality: {target_quality}p"
            )

        kb = get_quality_keyboard(
            available_qualities=metadata.available_qualities,
            url_hash=u_hash,
            current_quality=None if is_audio else target_quality,
            has_audio=metadata.has_audio,
        )

        input_file = FSInputFile(output_path, filename=output_path.name)

        if is_audio:
            await message.reply_audio(
                audio=input_file,
                caption=caption,
                title=metadata.title,
                performer=metadata.uploader,
                reply_markup=kb,
                parse_mode="HTML",
            )
        else:
            await message.reply_video(
                video=input_file,
                caption=caption,
                reply_markup=kb,
                parse_mode="HTML",
            )

        # Log to Database
        try:
            async with AsyncSessionLocal() as session:
                repo = Repository(session)
                await repo.get_or_create_user(user_id, message.from_user.username)
                await repo.log_download(
                    user_id=user_id,
                    chat_id=chat_id,
                    chat_type=message.chat.type,
                    url=url,
                    title=metadata.title,
                    quality="audio" if is_audio else f"{target_quality}p",
                    format_name="mp3" if is_audio else "mp4",
                    file_size=output_path.stat().st_size if output_path.exists() else 0,
                    status="completed",
                )
        except Exception as dbe:
            logger.warning("Failed to record download in DB: %s", dbe)

        # Delete status message on success
        try:
            await status_msg.delete()
        except Exception:
            pass

    except RuntimeError as re:
        if "cancelled" in str(re).lower():
            await status_msg.edit_text("❌ Download cancelled.")
        else:
            await status_msg.edit_text("❌ Download failed. Please try again later.")
    except Exception as e:
        logger.error("Download error for %s: %s", url, e)
        await status_msg.edit_text(
            "❌ Download failed.\n\n"
            "The link may be unsupported, unavailable, private, or temporarily inaccessible."
        )

    finally:
        active_jobs.pop(job.job_id, None)
        await rate_limiter.release(user_id, chat_id, is_group)
        if job.job_dir:
            cleanup_job_directory(job.job_dir)


async def _safe_edit_message(msg: Message, text: str, reply_markup=None) -> None:
    """Helper to safely edit message text suppressingTelegram edit errors."""
    try:
        await msg.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        pass


@router.message(F.text & ~F.text.startswith("/"))
async def handle_url_message(message: Message) -> None:
    """Handle plain messages containing video URLs."""
    url = find_first_url(message.text)
    if not url:
        return

    logger.info("URL detected in chat %s from user %s: %s", message.chat.id, message.from_user.id if message.from_user else 0, url)

    # Validate URL
    is_valid, reason = validate_download_url(url)
    if not is_valid:
        await message.reply(f"❌ {reason}")
        return

    # Trigger automatic 720p download
    await process_media_download(message=message, url=url, target_quality=720, is_audio=False)
