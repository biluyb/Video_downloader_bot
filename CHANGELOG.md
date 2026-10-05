# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] — 2026-10-05

### Added — Core Download Engine & Features (FEATURE-002 through FEATURE-012)

- **FEATURE-002: Secure URL Detection & Validation**
  - Regex-based URL extraction from plain text and group messages (`app/utils/url_extractor.py`)
  - Scheme validation & SSRF protection against private IPs, localhost, and restricted hosts (`app/utils/validators.py`)
- **FEATURE-003: Metadata Extraction**
  - Async video metadata extraction using yt-dlp (`app/services/metadata.py`)
- **FEATURE-004: Automatic 720p Download**
  - Automatic 720p download engine with automatic fallback to best available quality below 720p (`app/services/downloader.py`)
  - Isolated job directory execution under `downloads/job_<uuid>/`
  - Guaranteed cleanup via `app/services/cleanup.py`
- **FEATURE-005: Quality Selection UI**
  - Dynamic inline quality keyboard generation displaying only existing heights (`app/keyboards/quality.py`)
  - Callbacks for quality selection (1080p, 720p, 480p, 360p)
- **FEATURE-006: Audio Download**
  - MP3 audio download & extraction (`[🎵 Audio (MP3)]` button)
- **FEATURE-007: Progress UI**
  - Real-time status update message with progress bar, download speed, and ETA calculation
- **FEATURE-008: Group Support**
  - Automatic link detection in group chats without needing `/download` command or bot mentions
- **FEATURE-009: Cancellation**
  - `[❌ Cancel Download]` button in progress UI
- **FEATURE-010: Concurrency Queue**
  - Concurrency management using asyncio semaphore (`app/services/queue.py`)
- **FEATURE-011: Rate Limiting**
  - Per-user and per-group concurrency and hourly download rate limiting (`app/services/rate_limiter.py`)
- **FEATURE-012: Database & History**
  - SQLite + SQLAlchemy async ORM models (`User`, `DownloadRecord`)
  - `/history` command showing recent downloads

## [0.1.0] — 2026-10-05

### Added — FEATURE-001: Bot Foundation

- Project structure following clean architecture
- `/start`, `/help`, `/about` command handlers
- Test suite and initial documentation
