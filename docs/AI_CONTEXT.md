# AI Context — Download Via Link

> This file is the persistent context for AI developers working on this project.
> **NEVER put the actual BOT_TOKEN in this file.**

## Bot Identity

- **Bot Name:** Download Via Link
- **Telegram Username:** `@lookvidbot`
- **Telegram Link:** [https://t.me/lookvidbot](https://t.me/lookvidbot)
- **Brand:** LookVid

## GitHub Repository

```
https://github.com/biluyb/Video_downloader_bot.git
```

## Current Status

**Version:** 0.2.0

**Completed Features:** FEATURE-001 through FEATURE-012 ✅

**Git Branch:** `feature/video-download`

## Architecture

- **Framework:** aiogram 3.x (async Telegram bot framework)
- **Language:** Python 3.12+
- **Media Extraction:** yt-dlp
- **Media Processing:** static-ffmpeg (FFmpeg n8.0.1)
- **Configuration:** pydantic-settings loading from `.env`
- **Database:** SQLite via SQLAlchemy 2.0 (asyncio + aiosqlite)
- **Logging:** Structured logging via `app/utils/logger.py`

### Module Layout

```
app/
├── main.py              — Entry point, token validation, router registration, DB & FFmpeg init
├── config/settings.py   — Pydantic settings from environment
├── handlers/
│   ├── start.py         — /start command
│   ├── help.py          — /help and /about commands
│   ├── history.py       — /history command (download history)
│   ├── callbacks.py     — Inline button callbacks (qualities, audio, cancel)
│   └── download.py      — URL detection, progress UI, downloader orchestration
├── keyboards/
│   ├── main.py          — Start, help, back keyboards
│   └── quality.py       — Dynamic quality selection & cancel keyboards
├── services/
│   ├── downloader.py    — Isolated job downloading via yt-dlp & progress tracking
│   ├── metadata.py      — Media info & available qualities extraction
│   ├── cleanup.py       — Job directory cleanup
│   ├── rate_limiter.py  — Per-user, per-group, hourly rate limiting
│   └── queue.py         — Concurrency control semaphore
├── database/
│   ├── database.py      — Async engine & session factory
│   ├── models.py        — User & DownloadRecord SQLAlchemy models
│   └── repositories.py  — Database repository CRUD
└── utils/
    ├── logger.py        — Logging setup
    ├── validators.py    — URL scheme validation & SSRF protection
    ├── url_extractor.py — Text URL extraction
    └── formatters.py    — String & speed formatters
```

## Completed Features

### FEATURE-001: Bot Foundation ✅
- Project structure matching the architecture spec
- `/start`, `/help`, `/about` commands

### FEATURE-002: URL Detection & Validation ✅
- Text & message URL extraction
- HTTP/HTTPS scheme validation
- SSRF protection (localhost, private IP rejection, DNS lookup check)

### FEATURE-003: Metadata Extraction ✅
- yt-dlp video metadata extraction (title, duration, uploader, available qualities)

### FEATURE-004: Automatic 720p Download ✅
- Default 720p download
- Automatic fallback if 720p is unavailable (e.g. 480p)
- Upload to Telegram (video/audio)

### FEATURE-005: Quality Selection UI ✅
- Inline quality keyboard showing only available formats (1080p, 720p, 480p, 360p)

### FEATURE-006: Audio Download ✅
- MP3 audio extraction & audio tag formatting

### FEATURE-007: Progress UI ✅
- Live status message with progress bar (`████████░░ 80%`), download speed, and ETA

### FEATURE-008: Group Support ✅
- Automatic URL detection in private & group messages without requiring commands or bot mentions

### FEATURE-009: Cancellation ✅
- `[❌ Cancel Download]` button in progress UI

### FEATURE-010: Download Queue & Concurrency ✅
- Global semaphore concurrency control (`MAX_CONCURRENT_DOWNLOADS=2`)

### FEATURE-011: Rate Limiting ✅
- Per-user and per-group concurrency limits & hourly request limits

### FEATURE-012: Database & History ✅
- SQLite + SQLAlchemy async ORM, `/history` command

## Environment Variables

See `.env.example` for all variables. Key ones:

- `BOT_TOKEN` — Telegram bot token (from @BotFather)
- `DATABASE_URL` — `sqlite+aiosqlite:///./data/bot.db`
- `TEMP_DIR` — Temporary download directory (`./downloads`)
- `MAX_CONCURRENT_DOWNLOADS` — Global concurrency limit (default: 2)

## Telegram Privacy

For group functionality, BotFather privacy mode must be **disabled**:
```
/setprivacy → Select bot → Disable
```
The bot does NOT require administrator permissions.

## Testing Status

- ✅ 41 tests passing across all modules (settings, handlers, validators, extractor, downloader, rate limiter, database)
