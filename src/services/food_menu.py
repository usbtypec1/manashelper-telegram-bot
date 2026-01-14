import datetime
from zoneinfo import ZoneInfo

from models.food_menu import DailyMenu
from repositories.food_menu import FoodMenuRepository


class FoodMenuService:

    def __init__(self, food_menu_repository: FoodMenuRepository):
        self.__food_menu_repository = food_menu_repository

    async def get_food_menu(
        self,
        *,
        days_to_skip: int,
    ) -> DailyMenu:
        timezone = ZoneInfo("Asia/Bishkek")
        date = datetime.datetime.now(timezone) + datetime.timedelta(
            days=days_to_skip,
        )
        return await self.__food_menu_repository.get_food_menu(date=date)
