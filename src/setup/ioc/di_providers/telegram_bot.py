from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from setup.config.telegram_bot import TelegramBotToken


class TelegramBotProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_telegram_bot(self, token: TelegramBotToken) -> Bot:
        return Bot(
            token=token.get_secret_value(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
        )

    @provide
    def provide_dispatcher(self) -> Dispatcher:
        return Dispatcher()
