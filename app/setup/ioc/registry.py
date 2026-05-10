from dishka import Provider

from app.setup.ioc.di_providers.repositories import repository_provider
from app.setup.ioc.di_providers.services import service_provider
from app.setup.ioc.di_providers.settings import SettingsProvider


def get_providers() -> tuple[Provider, ...]:
    return (
        repository_provider(),
        service_provider(),
        SettingsProvider(),
    )
