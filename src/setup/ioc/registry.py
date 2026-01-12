from dishka import Provider

from setup.ioc.di_providers.repositories import repository_provider
from setup.ioc.di_providers.services import service_provider
from setup.ioc.di_providers.settings import SettingsProvider
from setup.ioc.di_providers.telegram_bot import TelegramBotProvider


def get_providers() -> tuple[Provider, ...]:
    return (
        repository_provider(),
        service_provider(),
        SettingsProvider(),
        TelegramBotProvider(),
    )
