# Manashelper Telegram Bot

Telegram bot for the Manashelper project. Built with [aiogram](https://docs.aiogram.dev/) and wired together using [dishka](https://dishka.readthedocs.io/). The bot consumes a configurable API and exposes commands such as attendance, exams, timetable, and food menu.

## Features

- `/start` main menu
- `/yoklama` attendance lookup
- `/exams` exam score lookup
- Timetable and food menu flows

## Requirements

- Python 3.13+
- A Telegram bot token
- An HTTP API base URL for Manashelper

## Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
```

With `uv`:

```bash
uv sync
```

With `pip`:

```bash
pip install aiogram dishka httpx
```

## Configuration

Create a `settings.toml` in the repository root (next to `pyproject.toml`) with the following structure:

```toml
[telegram_bot]
# Telegram bot token from @BotFather
token = "YOUR_TELEGRAM_BOT_TOKEN"

[api]
# Base URL of the Manashelper HTTP API
base_url = "https://example.com/api"
```

## Running the bot

The code expects the `src` directory on the Python path. From the repository root:

```bash
PYTHONPATH=src python -m main
```

## Project layout

```
src/
  handlers/       # Telegram command and callback handlers
  services/       # Business logic, orchestration
  repositories/   # HTTP clients and data access
  setup/          # Dependency injection and configuration
  ui/             # Message rendering helpers
```

## Development notes

- Configuration is loaded from `settings.toml` via `AppSettings` in `setup/config/settings.py`.
- The bot starts polling in `src/main.py` and registers commands in `setup_commands`.
