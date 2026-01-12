from models.food_menu import DailyMenu
from repositories.food_menu import FoodMenuRepository


class FoodMenuService:

    def __init__(self, food_menu_repository: FoodMenuRepository):
        self.__food_menu_repository = food_menu_repository

    async def get_food_menu(self) -> list[DailyMenu]:
        return await self.__food_menu_repository.get_food_menu()
