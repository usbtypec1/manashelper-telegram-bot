from pydantic import TypeAdapter

from models.food_menu import DailyMenu
from repositories.error_handler import handle_api_errors
from repositories.http_client import ApiHttpClient


class FoodMenuRepository:

    def __init__(self, http_client: ApiHttpClient):
        self.__http_client = http_client

    async def get_food_menu(self) -> list[DailyMenu]:
        response = await self.__http_client.get("/food-menu")
        handle_api_errors(response)
        type_adapter = TypeAdapter(list[DailyMenu])
        return type_adapter.validate_json(response.text)
