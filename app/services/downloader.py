"""Downloader service integrating yt-dlp with progress tracking and job isolation."""

import asyncio
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Dict, Any
import static_ffmpeg

from app.config.settings import get_settings
from app.services.cleanup import cleanup_job_directory
from app.utils.logger import get_logger

logger = get_logger(__name__)

try:
    static_ffmpeg.add_paths()
except Exception as e:
    logger.warning("Could not set static_ffmpeg paths: %s", e)


@dataclass
class DownloadProgress:
    """Download progress state."""

    status: str = "downloading"  # downloading, processing, completed, cancelled, error
    percent: float = 0.0
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed_bytes_per_sec: float = 0.0
    eta_seconds: int = 0
    filename: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def formatted_speed(self) -> str:
        if self.speed_bytes_per_sec <= 0:
            return "0.0 MB/s"
        mb_per_sec = self.speed_bytes_per_sec / (1024 * 1024)
        return f"{mb_per_sec:.1f} MB/s"

    @property
    def formatted_eta(self) -> str:
        if self.eta_seconds <= 0:
            return "00:00"
        m, s = divmod(self.eta_seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"


ProgressCallback = Callable[[DownloadProgress], None]


class DownloadJob:
    """Represents a download task with isolated directory and cancellation support."""

    def __init__(self, url: str, target_quality: int = 720, is_audio: bool = False):
        self.job_id = f"job_{uuid.uuid4().hex[:12]}"
        self.url = url
        self.target_quality = target_quality
        self.is_audio = is_audio
        self.settings = get_settings()
        self.job_dir = self.settings.temp_path / self.job_id
        self.progress = DownloadProgress()
        self.cancelled = False

    def cancel(self) -> None:
        """Mark the job as cancelled."""
        self.cancelled = True
        self.progress.status = "cancelled"

    def _progress_hook(self, d: Dict[str, Any], callback: Optional[ProgressCallback] = None) -> None:
        if self.cancelled:
            raise RuntimeError("Download cancelled by user.")

        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes") or 0
            speed = d.get("speed") or 0.0
            eta = d.get("eta") or 0

            percent = (downloaded / total * 100) if total > 0 else 0.0

            self.progress.status = "downloading"
            self.progress.percent = percent
            self.progress.downloaded_bytes = downloaded
            self.progress.total_bytes = total
            self.progress.speed_bytes_per_sec = speed
            self.progress.eta_seconds = eta

            if callback:
                callback(self.progress)

        elif status == "finished":
            self.progress.status = "processing"
            self.progress.percent = 100.0
            if callback:
                callback(self.progress)

    def download_sync(self, callback: Optional[ProgressCallback] = None) -> Path:
        """Execute yt-dlp download synchronously."""
        import yt_dlp

        self.job_dir.mkdir(parents=True, exist_ok=True)
        outtmpl = str(self.job_dir / "%(title).200s.%(ext)s")

        if self.is_audio:
            format_str = "bestaudio/best"
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        else:
            # Video: format string selecting quality <= target_quality
            q = self.target_quality
            format_str = f"bestvideo[height<={q}]+bestaudio/best[height<={q}]/best"
            postprocessors = [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ]

        ydl_opts = {
            "format": format_str,
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [lambda d: self._progress_hook(d, callback)],
            "max_filesize": self.settings.max_file_size_bytes,
            "postprocessors": postprocessors,
            "socket_timeout": 30,
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
                ydl.download([self.url])
        except Exception as e:
            from app.services.tiktok_fallback import is_tiktok_url, fetch_tiktok_info_sync, download_file_sync
            if is_tiktok_url(self.url):
                logger.info("yt-dlp download failed for TikTok (%s), invoking TikTok fallback downloader...", e)
                tk_info = fetch_tiktok_info_sync(self.url)
                target_url = tk_info.audio_url if (self.is_audio and tk_info.audio_url) else tk_info.video_url
                ext = "mp3" if self.is_audio else "mp4"
                safe_title = "".join([c for c in tk_info.title if c.isalnum() or c in (" ", "-", "_")]).strip()[:50] or "tiktok_video"
                output_file = self.job_dir / f"{safe_title}.{ext}"
                download_file_sync(target_url, output_file)
                self.progress.status = "completed"
                self.progress.percent = 100.0
                self.progress.filename = output_file.name
                if callback:
                    callback(self.progress)
                return output_file
            raise

        if self.cancelled:
            raise RuntimeError("Download cancelled by user.")

        # Find the produced file in job_dir
        files = [f for f in self.job_dir.iterdir() if f.is_file() and not f.name.endswith(".part")]
        if not files:
            raise FileNotFoundError("No output media file produced by yt-dlp.")

        # Return largest file (in case of multiple temporary files)
        output_file = max(files, key=lambda f: f.stat().st_size)
        self.progress.status = "completed"
        self.progress.filename = output_file.name
        return output_file

    async def run(self, callback: Optional[ProgressCallback] = None) -> Path:
        """Run the download in an async thread pool."""
        logger.info("Starting download job %s for %s (quality: %s, audio: %s)", self.job_id, self.url, self.target_quality, self.is_audio)
        try:
            return await asyncio.to_thread(self.download_sync, callback)
        except Exception as e:
            logger.error("Download job %s failed: %s", self.job_id, e)
            self.progress.status = "error"
            self.progress.error_message = str(e)
            raise
