import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from exceptions.food_menu import DailyMenuRatingNotFoundException
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

    async def is_daily_menu_rated_by_user(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
    ) -> bool:
        try:
            await self.__food_menu_repository.get_daily_menu_rating(
                user_id=user_id,
                daily_menu_id=daily_menu_id,
            )
        except DailyMenuRatingNotFoundException:
            return False
        return True

    async def update_daily_menu_rating(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
        score: int,
    ) -> None:
        await self.__food_menu_repository.update_daily_menu_rating(
            user_id=user_id,
            daily_menu_id=daily_menu_id,
            score=score,
        )
