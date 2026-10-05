"""Metadata extraction service using yt-dlp."""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import static_ffmpeg

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Ensure ffmpeg paths are set
try:
    static_ffmpeg.add_paths()
except Exception as e:
    logger.warning("Could not set static_ffmpeg paths: %s", e)


@dataclass
class MediaMetadata:
    """Structured media metadata extracted from yt-dlp."""

    url: str
    title: str
    duration: int = 0
    uploader: str = "Unknown"
    extractor: str = "generic"
    available_qualities: List[int] = field(default_factory=list)
    has_audio: bool = True
    best_quality_720: int = 720
    is_720_available: bool = True
    thumbnail: Optional[str] = None

    @property
    def formatted_duration(self) -> str:
        """Format duration in seconds to MM:SS or HH:MM:SS."""
        if not self.duration:
            return "Unknown"
        m, s = divmod(self.duration, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"


def _extract_metadata_sync(url: str) -> MediaMetadata:
    """Synchronous metadata extraction using yt_dlp."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
        "socket_timeout": 20,
        "nocheckcertificate": True,
        "legacyserverconnect": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web", "mweb"]
            }
        },
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info: Dict[str, Any] = ydl.extract_info(url, download=False)
            if not info:
                raise ValueError("Failed to extract media information.")
    except Exception as e:
        from app.services.tiktok_fallback import is_tiktok_url, fetch_tiktok_info_sync
        if is_tiktok_url(url):
            logger.info("yt-dlp metadata failed for TikTok (%s), invoking TikTok fallback service...", e)
            tk_info = fetch_tiktok_info_sync(url)
            return MediaMetadata(
                url=url,
                title=tk_info.title,
                duration=tk_info.duration,
                uploader=tk_info.uploader,
                extractor="TikTok",
                available_qualities=[720],
                has_audio=True,
                best_quality_720=720,
                is_720_available=True,
                thumbnail=tk_info.cover_url,
            )
        raise

        # In case info is a playlist, select the first entry
        if "entries" in info and info["entries"]:
            info = info["entries"][0]

        title = info.get("title", "Untitled Video")
        duration = int(info.get("duration") or 0)
        uploader = info.get("uploader") or info.get("channel") or info.get("extractor", "Unknown")
        extractor = info.get("extractor_key") or info.get("extractor", "generic")
        thumbnail = info.get("thumbnail")

        # Extract available heights
        formats = info.get("formats", [])
        heights = set()
        has_audio = False

        for f in formats:
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            h = f.get("height")

            if acodec != "none":
                has_audio = True

            if h and isinstance(h, int) and vcodec != "none":
                heights.add(h)

        sorted_qualities = sorted(list(heights), reverse=True)

        # Standards: 1080p, 720p, 480p, 360p, 240p
        # Standardize available quality options to display
        standard_qualities = []
        for q in [1080, 720, 480, 360, 240]:
            # If standard quality or nearby height exists
            if any(abs(existing - q) <= 40 for existing in sorted_qualities):
                standard_qualities.append(q)

        if not standard_qualities:
            # Fallback if non-standard heights
            standard_qualities = sorted_qualities[:4] if sorted_qualities else [720]

        is_720 = 720 in standard_qualities or any(abs(h - 720) <= 40 for h in sorted_qualities)
        
        # Determine best available quality up to 720p
        qualities_le_720 = [q for q in standard_qualities if q <= 720]
        if qualities_le_720:
            best_720 = max(qualities_le_720)
        else:
            best_720 = min(standard_qualities) if standard_qualities else 720

        return MediaMetadata(
            url=url,
            title=title,
            duration=duration,
            uploader=uploader,
            extractor=extractor,
            available_qualities=standard_qualities,
            has_audio=has_audio,
            best_quality_720=best_720,
            is_720_available=is_720,
            thumbnail=thumbnail,
        )


async def extract_metadata(url: str) -> MediaMetadata:
    """Asynchronously extract metadata for a video URL.

    Args:
        url: Validated video URL.

    Returns:
        MediaMetadata instance.
    """
    logger.info("Extracting metadata for %s", url)
    return await asyncio.to_thread(_extract_metadata_sync, url)
