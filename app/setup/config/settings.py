import os

from pydantic import BaseModel, SecretStr, HttpUrl

from app.setup.config.telegram_bot import TelegramBotSettings, TelegramBotToken


class AppSettings(BaseModel):
    telegram_bot: TelegramBotSettings


def load_settings(
) -> AppSettings:
    return AppSettings(
        telegram_bot=TelegramBotSettings(
            token=TelegramBotToken(SecretStr(os.getenv("TELEGRAM_BOT_TOKEN"))),
            webhook_url=HttpUrl(os.getenv("TELEGRAM_BOT_WEBHOOK_URL")),
        )
    )
