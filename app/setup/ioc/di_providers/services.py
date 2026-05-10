from dishka import Provider, Scope

from app.services.food_menu import FoodMenuService
from app.services.timetable import TimetableService, TimetableServiceImpl
from app.services.user import UserService


def service_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=UserService)
    provider.provide(source=FoodMenuService)
    provider.provide(source=UserService)
    provider.provide(provides=TimetableService, source=TimetableServiceImpl)
    return provider
