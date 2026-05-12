from dishka import Provider, Scope

from app.services.food_menu import FoodMenuService, FoodMenuServiceImpl


def service_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(provides=FoodMenuService, source=FoodMenuServiceImpl)
    return provider
