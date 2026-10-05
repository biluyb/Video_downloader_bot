# Development Guide

## Prerequisites

- Python 3.12+
- pip
- Git
- FFmpeg (required for later features)

## Setup

```bash
# Clone
git clone https://github.com/biluyb/Video_downloader_bot.git
cd Video_downloader_bot

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Edit .env and set BOT_TOKEN
```

## Running the Bot

```bash
python -m app.main
```

## Running Tests

```bash
# All tests
pytest -v

# With coverage
pytest --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_handlers.py -v
```

## Project Conventions

### Code Style

- Use `ruff` for linting and formatting
- Type hints on all public functions
- Docstrings on all modules and classes
- Maximum line length: 88 characters

### Git Workflow

1. Create a feature branch: `git checkout -b feature/feature-name`
2. Make changes
3. Run tests: `pytest -v`
4. Check for secrets: `git diff --cached`
5. Commit with conventional commits: `feat: description`
6. Push and create PR

### Commit Convention

```
feat: add new feature
fix: fix a bug
docs: documentation changes
test: add or update tests
refactor: code restructuring
chore: maintenance tasks
```

### Security Checklist Before Commit

- [ ] No `.env` file staged
- [ ] No BOT_TOKEN in source code
- [ ] No API keys, passwords, or credentials
- [ ] No private keys
- [ ] `git diff --cached` reviewed

## Environment Variables

See `.env.example` for all available configuration options.

**NEVER** commit the `.env` file or any real tokens.
