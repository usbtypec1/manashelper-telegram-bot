from typing import NewType

from pydantic import BaseModel, SecretStr


TelegramBotToken = NewType("TelegramBotToken", SecretStr)


class TelegramBotSettings(BaseModel):
    token: TelegramBotToken
    webhook_url: str
