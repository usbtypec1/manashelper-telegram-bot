from dishka import Provider, Scope, provide, from_context
from pydantic import HttpUrl

from app.setup.config.settings import AppSettings
from app.setup.config.telegram_bot import TelegramBotToken


class SettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(AppSettings)

    @provide
    def provide_telegram_bot_token(
        self,
        settings: AppSettings,
    ) -> TelegramBotToken:
        return settings.telegram_bot.token

    @provide
    def provide_telegram_bot_webhook_url(
        self,
        settings: AppSettings,
    ) -> HttpUrl:
        return settings.telegram_bot.webhook_url
