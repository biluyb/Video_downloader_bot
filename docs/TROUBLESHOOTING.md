# Troubleshooting

## Bot doesn't start

### "BOT_TOKEN is not configured"
- Copy `.env.example` to `.env`
- Set `BOT_TOKEN` to your real BotFather token
- Make sure there are no extra spaces or quotes around the token

### Import errors
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Bot doesn't respond in groups

### Privacy mode not disabled
The most common issue. In BotFather:
1. Send `/setprivacy`
2. Select your bot
3. Choose `Disable`

Without this, the bot only receives `/commands` in groups, not regular messages containing URLs.

### Bot was added before privacy change
If you changed privacy mode after adding the bot to a group, **remove the bot from the group and re-add it**.

## Bot responds to /start but not to URLs

This is expected in FEATURE-001. URL detection is implemented in FEATURE-002. Download functionality is in FEATURE-004.

## Tests fail

### "No module named 'app'"
Run tests from the project root:
```bash
cd Video_downloader_bot
pytest -v
```

### Tests accidentally use real token
The `conftest.py` fixture sets `BOT_TOKEN=test_token_12345` for all tests. If tests are using your real token, make sure `conftest.py` exists in the `tests/` directory.

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Unauthorized` | Invalid bot token | Check BOT_TOKEN in .env |
| `Conflict: terminated by other getUpdates request` | Another instance is running | Stop the other instance |
| `ModuleNotFoundError` | Dependencies not installed | `pip install -r requirements.txt` |
