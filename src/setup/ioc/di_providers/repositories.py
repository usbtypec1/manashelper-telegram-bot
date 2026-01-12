from dishka import Provider, Scope

from repositories.food_menu import FoodMenuRepository
from repositories.http_client import get_api_http_client
from repositories.user import UserRepository


def repository_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=get_api_http_client)
    provider.provide(source=FoodMenuRepository)
    provider.provide(source=UserRepository)
    return provider
