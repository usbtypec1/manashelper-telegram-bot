import datetime
from uuid import UUID

from app.models.food_menu import DailyMenu, DailyMenuRating


class FoodMenuRepository:

    async def get_food_menu(
        self,
        date: datetime.date,
    ) -> DailyMenu:
        raise NotImplementedError

    async def get_daily_menu_rating(
        self,
        *,
        daily_menu_id: UUID,
        user_id: int | None = None,
    ) -> list[DailyMenuRating]:
        raise NotImplementedError

    async def update_daily_menu_rating(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
        score: int,
        comment: str | None = None,
    ) -> None:
        pass
