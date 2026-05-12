from dishka import Provider

from app.setup.ioc.di_providers.services import service_provider


def get_providers() -> tuple[Provider, ...]:
    return (
        service_provider(),
    )
