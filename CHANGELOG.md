# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] — 2026-10-05

### Added — FEATURE-001: Bot Foundation

- Project structure following clean architecture
- `app/config/settings.py` — Pydantic-settings configuration from `.env`
- `app/handlers/start.py` — `/start` command with welcome message
- `app/handlers/help.py` — `/help` and `/about` commands
- `app/handlers/callbacks.py` — Inline button navigation (Help ↔ About ↔ Start)
- `app/keyboards/main.py` — Inline keyboard layouts
- `app/utils/logger.py` — Centralised structured logging
- `app/main.py` — Bot entry point with token validation
- `.env.example` — Environment variable template
- `.gitignore` — Comprehensive ignore rules
- `requirements.txt` — Python dependencies
- Test suite: settings, handlers, keyboards, logging, main validation
- Documentation: README, PROJECT, ARCHITECTURE, DEVELOPMENT, SECURITY, DEPLOYMENT, TROUBLESHOOTING, AI_CONTEXT
- Placeholder modules for services, database, and future features
