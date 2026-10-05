# Architecture

## High-Level Data Flow

```
                    Telegram
                       │
             ┌─────────┴─────────┐
             │                   │
        Private Chat          Group Chat
             │                   │
             └─────────┬─────────┘
                       ↓
                  aiogram 3.x
                       ↓
                Message Handler
                       ↓
                 URL Detector
                       ↓
                URL Validator
                       ↓
               Metadata Service
                       ↓
                 Download Queue
                       ↓
                    Worker
                       ↓
                   yt-dlp
                       ↓
                   FFmpeg
                       ↓
              Temporary Storage
                       ↓
              Telegram Upload
                       ↓
                   Cleanup
```

## Module Responsibilities

### `app/config/`
- Load and validate all settings from environment variables
- Centralised configuration via `pydantic-settings`
- Single source of truth for all tunables

### `app/handlers/`
- Telegram-specific message and callback handling
- Translate Telegram events into service calls
- No business logic — just orchestration

### `app/keyboards/`
- Inline keyboard construction
- Separated from handlers for reusability

### `app/services/`
- Pure business logic, no Telegram dependency
- `downloader.py` — yt-dlp integration
- `metadata.py` — Video metadata extraction
- `media.py` — FFmpeg audio/video processing
- `queue.py` — asyncio.Queue-based job scheduling
- `cleanup.py` — Temporary file management
- `rate_limiter.py` — Per-user, per-group, global limits
- `security.py` — URL validation, SSRF protection

### `app/database/`
- SQLAlchemy ORM models and repositories
- Database connection management
- Designed for SQLite now, PostgreSQL later

### `app/utils/`
- Cross-cutting concerns
- Logging, URL extraction, input validation, text formatting

## Design Principles

1. **Separation of concerns** — Telegram logic ≠ business logic
2. **Async-first** — Everything runs on asyncio
3. **Configuration over hardcoding** — All limits are env-configurable
4. **Security by default** — URL validation, SSRF protection, no shell commands
5. **Clean failure** — Users see friendly errors; technical details go to logs
6. **Guaranteed cleanup** — Temp files are always removed via try/finally
