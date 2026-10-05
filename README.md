# Video_downloader_bot

**Download Via Link** — A Telegram bot that downloads videos from YouTube, TikTok, Instagram, Facebook, X, Reddit, Vimeo, and many other platforms.

**Bot:** [@lookvidbot](https://t.me/lookvidbot)

## ✨ Features

- 🔗 Send a video link → automatic 720p download
- 📺 Quality options: 1080p, 720p, 480p, 360p
- 🎵 Audio download (MP3)
- 👥 Works in groups — no commands needed
- ⚡ Fast & simple

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- FFmpeg (for audio/video processing — needed for later features)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/biluyb/Video_downloader_bot.git
   cd Video_downloader_bot
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).

5. **Configure BotFather privacy (for group support):**
   - Open [@BotFather](https://t.me/BotFather)
   - Send `/setprivacy`
   - Select your bot
   - Choose `Disable`
   
   This allows the bot to read messages in groups for automatic URL detection.

6. **Run the bot:**
   ```bash
   python -m app.main
   ```

### Running Tests

```bash
pytest -v
```

## 📁 Project Structure

```
Video_downloader_bot/
├── app/
│   ├── main.py              # Entry point
│   ├── config/settings.py   # Environment configuration
│   ├── handlers/            # Telegram command handlers
│   ├── keyboards/           # Inline keyboard layouts
│   ├── services/            # Business logic (future)
│   ├── database/            # Data layer (future)
│   └── utils/               # Logging, validators, helpers
├── tests/                   # pytest test suite
├── docs/                    # Documentation
├── downloads/               # Temporary download directory
├── data/                    # SQLite database
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

## 🔐 Security

- Bot token is loaded from environment variables only
- Never commit `.env` or real tokens
- See [docs/SECURITY.md](docs/SECURITY.md) for the full security model

## 📖 Documentation

| Document | Description |
|---|---|
| [PROJECT.md](docs/PROJECT.md) | Project overview |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Development guide |
| [SECURITY.md](docs/SECURITY.md) | Security policies |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guide |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues |
| [AI_CONTEXT.md](docs/AI_CONTEXT.md) | AI developer context |

## 📄 License

This project is private.
