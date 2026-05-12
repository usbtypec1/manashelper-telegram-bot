from aiogram.filters.callback_data import CallbackData


class FoodMenuCallbackData(CallbackData, prefix="food_menu"):
    days_to_skip: int
