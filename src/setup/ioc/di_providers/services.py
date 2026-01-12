from dishka import Provider, Scope

from services.food_menu import FoodMenuService
from services.user import UserService


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(source=UserService, scope=Scope.REQUEST)
    provider.provide(source=FoodMenuService, scope=Scope.REQUEST)
    return provider
