# Deployment

## Local Development

```bash
# 1. Clone and setup
git clone https://github.com/biluyb/Video_downloader_bot.git
cd Video_downloader_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env — set BOT_TOKEN from @BotFather

# 3. Configure BotFather privacy
# Open @BotFather → /setprivacy → Select bot → Disable
# This is REQUIRED for group URL auto-detection

# 4. Run
python -m app.main
```

## BotFather Setup

1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` (or use existing bot)
3. Copy the token
4. Set in `.env` as `BOT_TOKEN=your_token_here`

### Privacy Mode (Required for Groups)

```
/setprivacy → Select bot → Disable
```

This lets the bot see normal messages in groups so it can detect URLs automatically. Without this, the bot can only see commands (messages starting with `/`).

**Note:** The bot does **not** need to be a group administrator for basic downloading. It only needs privacy mode disabled.

## Docker (FEATURE-014)

Docker deployment will be added in FEATURE-014.

```bash
# Coming soon
docker-compose up -d
```

## Environment Variables

See `.env.example` for all configurable values.

**Security reminder:** Never commit `.env` to version control.

## System Requirements

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |
| FFmpeg | Latest stable |
| RAM | 512 MB |
| Disk | 2 GB free (for temporary downloads) |
| Network | Outbound HTTPS |
