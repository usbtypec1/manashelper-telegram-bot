import datetime
from uuid import UUID

from models.food_menu import DailyMenu, DailyMenuRating
from repositories.error_handler import handle_api_errors
from repositories.http_client import ApiHttpClient


class FoodMenuRepository:

    def __init__(self, http_client: ApiHttpClient):
        self.__http_client = http_client

    async def get_food_menu(
        self,
        date: datetime.date,
    ) -> DailyMenu:
        params = {"date": f'{date:%Y-%m-%d}'}
        response = await self.__http_client.get("/food-menu", params=params)
        handle_api_errors(response)
        return DailyMenu.model_validate_json(response.text)

    async def get_daily_menu_rating(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
    ) -> DailyMenuRating:
        url = f"/food-menu/{daily_menu_id}/ratings/users/{user_id}"
        response = await self.__http_client.get(url)
        handle_api_errors(response)
        return DailyMenuRating.model_validate_json(response.text)

    async def update_daily_menu_rating(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
        score: int,
        comment: str | None = None,
    ) -> None:
        url = f"/food-menu/{daily_menu_id}/ratings"
        request_data = {"score": score, "userId": user_id, "comment": comment}
        response = await self.__http_client.put(url, json=request_data)
        handle_api_errors(response)
