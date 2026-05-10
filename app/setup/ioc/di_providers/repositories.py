from dishka import Provider, Scope

from repositories.food_menu import FoodMenuRepository
from repositories.timetable import TimetableRepository
from repositories.user import UserRepository


def repository_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(source=FoodMenuRepository)
    provider.provide(source=UserRepository)
    provider.provide(source=TimetableRepository)
    return provider
