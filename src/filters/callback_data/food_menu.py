from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class FoodMenuCallbackData(CallbackData, prefix="food_menu"):
    days_to_skip: int


class DailyMenuRatingCallbackData(CallbackData, prefix="daily_menu_rating"):
    daily_menu_id: UUID
    score: int


class DailyMenuCommentCallbackData(CallbackData, prefix="daily_menu_comment"):
    daily_menu_id: UUID
    score: int
