# Project Overview

## Download Via Link — @lookvidbot

**Brand:** LookVid

**Bot Username:** `@lookvidbot`

**Telegram Link:** [https://t.me/lookvidbot](https://t.me/lookvidbot)

**GitHub:** [https://github.com/biluyb/Video_downloader_bot.git](https://github.com/biluyb/Video_downloader_bot.git)

## Description

Download videos from YouTube, TikTok, Instagram, Facebook, X, Reddit, Vimeo, and many other supported platforms. 720p is the default, with 1080p, 480p, 360p, and other available qualities when supported. Audio download is also available.

## Core UX Principle

The user should not have to think.

### Private Chat

```
User → Paste link → Automatic 720p download → Video → Quality options
```

### Group Chat

```
User sends link → Bot auto-detects → Downloads 720p → Posts video → Quality options
```

No commands required. No quality selection before the first download.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| Bot framework | aiogram 3.x |
| Video extraction | yt-dlp |
| Audio/video processing | FFmpeg |
| Async runtime | asyncio |
| Database ORM | SQLAlchemy 2.x |
| Database | SQLite (PostgreSQL-ready) |
| Configuration | pydantic-settings |
| Testing | pytest |
| Containerisation | Docker |

## Feature Roadmap

| ID | Feature | Status |
|---|---|---|
| FEATURE-001 | Bot Foundation | ✅ Complete |
| FEATURE-002 | URL Detection & Validation | 🔲 Planned |
| FEATURE-003 | Metadata Extraction | 🔲 Planned |
| FEATURE-004 | Automatic 720p Download | 🔲 Planned |
| FEATURE-005 | Quality Selection | 🔲 Planned |
| FEATURE-006 | Audio Download | 🔲 Planned |
| FEATURE-007 | Progress UI | 🔲 Planned |
| FEATURE-008 | Group Support | 🔲 Planned |
| FEATURE-009 | Cancellation | 🔲 Planned |
| FEATURE-010 | Download Queue | 🔲 Planned |
| FEATURE-011 | Rate Limiting | 🔲 Planned |
| FEATURE-012 | Database & History | 🔲 Planned |
| FEATURE-013 | Security Hardening | 🔲 Planned |
| FEATURE-014 | Docker & Production | 🔲 Planned |

## BotFather Privacy Configuration

For group support, the bot requires **privacy mode disabled** in BotFather:

1. Open [@BotFather](https://t.me/BotFather)
2. Send `/setprivacy`
3. Select your bot
4. Choose `Disable`

This allows the bot to receive normal messages in groups for automatic URL detection. The bot does **not** require administrator permissions for basic downloading.
