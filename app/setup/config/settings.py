import os
from typing import NewType

from pydantic import BaseModel, SecretStr

from app.setup.config.telegram_bot import TelegramBotSettings, TelegramBotToken

MongodbUri = NewType("MongodbUri", str)


class AppSettings(BaseModel):
    telegram_bot: TelegramBotSettings
    mongodb_url: str


def load_settings(
) -> AppSettings:
    return AppSettings(
        telegram_bot=TelegramBotSettings(
            token=TelegramBotToken(SecretStr(os.getenv("TELEGRAM_BOT_TOKEN"))),
            webhook_url=os.getenv("TELEGRAM_BOT_WEBHOOK_URL"),
        ),
        mongodb_url=MongodbUri(os.getenv("MONGODB_URI")),
    )
