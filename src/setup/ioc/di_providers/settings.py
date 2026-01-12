from dishka import Provider, Scope, provide, from_context

from repositories.http_client import ApiBaseUrl
from setup.config.settings import AppSettings
from setup.config.telegram_bot import TelegramBotToken


class SettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(AppSettings)

    @provide
    def provide_api_base_url(self, settings: AppSettings) -> ApiBaseUrl:
        return settings.api.base_url

    @provide
    def provide_telegram_bot_token(
        self,
        settings: AppSettings,
    ) -> TelegramBotToken:
        return settings.telegram_bot.token
