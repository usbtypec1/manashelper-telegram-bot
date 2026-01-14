import datetime

from models.food_menu import DailyMenu
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

