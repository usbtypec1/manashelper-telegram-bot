from dishka import Provider, Scope

from services.food_menu import FoodMenuService
from services.timetable import TimetableService
from services.user import UserService


def service_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=UserService)
    provider.provide(source=FoodMenuService)
    provider.provide(source=UserService)
    provider.provide(source=TimetableService)
    return provider
