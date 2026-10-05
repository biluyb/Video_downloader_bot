"""TikTok fallback extractor service for bypassing HTTP 403 errors on yt-dlp."""

import asyncio
import json
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.services.metadata import MediaMetadata
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class TikTokMediaInfo:
    """TikTok video details extracted via API fallback."""
    title: str
    uploader: str
    duration: int
    video_url: str
    audio_url: Optional[str] = None
    cover_url: Optional[str] = None


def is_tiktok_url(url: str) -> bool:
    """Check if URL is a TikTok video link."""
    domain = urllib.parse.urlparse(url).netloc.lower()
    return any(d in domain for d in ["tiktok.com", "vt.tiktok.com", "vm.tiktok.com"])


def fetch_tiktok_info_sync(url: str) -> TikTokMediaInfo:
    """Synchronously fetch TikTok video info via TikWM API."""
    api_endpoint = f"https://www.tikwm.com/api/?url={urllib.parse.quote(url)}"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        api_endpoint,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode("utf-8")
        payload = json.loads(content)

    code = payload.get("code")
    if code != 0 or "data" not in payload:
        msg = payload.get("msg") or "Failed to fetch TikTok media via fallback API."
        raise ValueError(msg)

    data = payload["data"]
    title = data.get("title") or "TikTok Video"
    uploader = data.get("author", {}).get("nickname") or data.get("author", {}).get("unique_id") or "TikTok Creator"
    duration = int(data.get("duration") or 0)
    
    # Prefer HD play link if available, fallback to standard play link
    video_url = data.get("hdplay") or data.get("play") or data.get("wmplay")
    if not video_url:
        raise ValueError("No valid video stream URL found in TikTok fallback API.")

    if not video_url.startswith("http"):
        video_url = f"https://www.tikwm.com{video_url}"

    audio_url = data.get("music")
    cover_url = data.get("cover")

    return TikTokMediaInfo(
        title=title,
        uploader=uploader,
        duration=duration,
        video_url=video_url,
        audio_url=audio_url,
        cover_url=cover_url,
    )


async def fetch_tiktok_info(url: str) -> TikTokMediaInfo:
    """Asynchronously fetch TikTok media info."""
    return await asyncio.to_thread(fetch_tiktok_info_sync, url)


def download_file_sync(file_url: str, output_path: Path) -> Path:
    """Synchronously download media file from direct URL."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        file_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        },
    )

    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp, open(output_path, "wb") as f:
        while chunk := resp.read(65536):
            f.write(chunk)

    return output_path


async def download_direct_file(file_url: str, output_path: Path) -> Path:
    """Asynchronously download direct file to target path."""
    return await asyncio.to_thread(download_file_sync, file_url, output_path)
