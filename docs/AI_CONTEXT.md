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

**Version:** 0.1.0

**Current Feature:** FEATURE-001 — Bot Foundation ✅ COMPLETE

**Git Branch:** `feature/bot-foundation`

**Latest Commit:** `feat: add telegram bot foundation (FEATURE-001)`

## Architecture

- **Framework:** aiogram 3.x (async Telegram bot framework)
- **Language:** Python 3.12+
- **Configuration:** pydantic-settings loading from `.env`
- **Database:** SQLite via SQLAlchemy (planned for FEATURE-012)
- **Logging:** Structured logging via `app/utils/logger.py`

### Module Layout

```
app/
├── main.py              — Entry point, token validation, router registration
├── config/settings.py   — Pydantic settings from environment
├── handlers/
│   ├── start.py         — /start command
│   ├── help.py          — /help and /about commands
│   ├── callbacks.py     — Inline button callbacks
│   ├── download.py      — (placeholder)
│   └── history.py       — (placeholder)
├── keyboards/
│   ├── main.py          — Start, help, back keyboards
│   └── quality.py       — (placeholder)
├── services/            — Business logic (all placeholders)
├── database/            — Data layer (all placeholders)
└── utils/
    ├── logger.py        — Logging setup
    ├── validators.py    — (placeholder)
    ├── url_extractor.py — (placeholder)
    └── formatters.py    — (placeholder)
```

## Completed Features

### FEATURE-001: Bot Foundation ✅
- Project structure matching the architecture spec
- pydantic-settings configuration from `.env`
- aiogram 3.x setup with long-polling
- `/start` with welcome text + Help/About buttons
- `/help` with usage instructions
- `/about` with bot description
- Inline callback navigation (Help ↔ About ↔ Start)
- Centralised structured logging
- Token validation at startup (rejects placeholder)
- Test suite (settings, handlers, keyboards, logging, main validation)
- Full documentation suite
- `.env.example`, `.gitignore`

## Pending Features (in order)

| Feature | Description |
|---|---|
| FEATURE-002 | Secure URL Detection & Validation |
| FEATURE-003 | Metadata Extraction (yt-dlp) |
| FEATURE-004 | Automatic 720p Download |
| FEATURE-005 | Quality Selection UI |
| FEATURE-006 | Audio Download (MP3) |
| FEATURE-007 | Progress UI |
| FEATURE-008 | Group Support |
| FEATURE-009 | Cancellation |
| FEATURE-010 | Download Queue |
| FEATURE-011 | Rate Limiting |
| FEATURE-012 | Database & History |
| FEATURE-013 | Security Hardening |
| FEATURE-014 | Docker & Production |

## Environment Variables

See `.env.example` for all variables. Key ones:

- `BOT_TOKEN` — Telegram bot token (from @BotFather)
- `DATABASE_URL` — SQLAlchemy connection string
- `TEMP_DIR` — Temporary download directory
- `MAX_CONCURRENT_DOWNLOADS` — Global concurrency limit
- `LOG_LEVEL` — Logging verbosity

## Security Decisions

1. Token loaded from env only — never in source code
2. Placeholder token rejected at startup
3. All future subprocesses will use `asyncio.create_subprocess_exec` (no shell=True)
4. URL validation will reject dangerous schemes, private IPs, SSRF vectors
5. User-provided filenames never used as filesystem paths
6. Temp files cleaned via try/finally

## Telegram Privacy

For group functionality, BotFather privacy mode must be **disabled**:
```
/setprivacy → Select bot → Disable
```
The bot does NOT require administrator permissions.

## Known Limitations

- No download functionality yet (FEATURE-004)
- No URL detection yet (FEATURE-002)
- No database yet (FEATURE-012)
- No Docker yet (FEATURE-014)

## Testing Status

- ✅ Settings loading & defaults
- ✅ Handler text content
- ✅ Keyboard structure
- ✅ Logging configuration
- ✅ Token validation logic

## Next Recommended Feature

**FEATURE-002 — Secure URL Detection & Validation**

Implement:
- URL extraction from messages (plain text and embedded)
- HTTP/HTTPS scheme validation
- Supported platform detection
- SSRF protection (private IP, localhost rejection)
- Dangerous scheme rejection
- Security tests
