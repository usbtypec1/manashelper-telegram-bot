from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka

from exceptions.food_menu import DailyMenuNotFoundException
from filters.callback_data.food_menu import (
    FoodMenuCallbackData,
    DailyMenuRatingCallbackData,
)
from services.food_menu import FoodMenuService
from ui.views.base import answer_media_group_view, answer_view
from ui.views.food_menu import DailyMenuView, DailyMenuRateSuggestionView


food_menu_router = Router(name=__name__)


@food_menu_router.callback_query(DailyMenuRatingCallbackData.filter())
async def on_daily_menu_rating_callback_query(
    callback_query: CallbackQuery,
    callback_data: DailyMenuRatingCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    await food_menu_service.update_daily_menu_rating(
        user_id=callback_query.from_user.id,
        daily_menu_id=callback_data.daily_menu_id,
        score=callback_data.score,
    )
    await callback_query.answer(
        text="Спасибо за вашу оценку! ❤️",
        show_alert=True,
    )
    if callback_query.message.chat.type == ChatType.PRIVATE:
        await callback_query.message.edit_text(
            f"Вы поставили оценку {callback_data.score} ⭐️",
        )


@food_menu_router.callback_query(FoodMenuCallbackData.filter())
async def on_food_menu_callback_query(
    callback_query: CallbackQuery,
    callback_data: FoodMenuCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    try:
        daily_menu = await food_menu_service.get_food_menu(
            days_to_skip=callback_data.days_to_skip,
        )
    except DailyMenuNotFoundException:
        await callback_query.answer(
            "Меню на этот день недоступно 😔",
            show_alert=True,
        )
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=callback_query.message, view=view)
    await callback_query.answer("")

    is_daily_menu_rated = await food_menu_service.is_daily_menu_rated_by_user(
        user_id=callback_query.from_user.id,
        daily_menu_id=daily_menu.id,
    )
    if not is_daily_menu_rated:
        view = DailyMenuRateSuggestionView(daily_menu_id=daily_menu.id)
        await answer_view(callback_query.message, view)


@food_menu_router.message(Command("yemek"))
async def on_food_menu_command(
    message: Message,
    command: CommandObject,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    if not command.args:
        return

    word_to_days_count = {
        "today": 0,
        "tomorrow": 1,
    }

    if command.args in word_to_days_count:
        days_to_skip = word_to_days_count[command.args]
    elif command.args.isdigit():
        days_to_skip = int(command.args)
    else:
        await message.reply("Не могу распознать день 😔")
        return

    try:
        daily_menu = await food_menu_service.get_food_menu(
            days_to_skip=days_to_skip,
        )
    except DailyMenuNotFoundException:
        await message.answer(
            "Меню на этот день недоступно 😔",
            show_alert=True,
        )
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=message, view=view)

    is_daily_menu_rated = await food_menu_service.is_daily_menu_rated_by_user(
        user_id=message.from_user.id,
        daily_menu_id=daily_menu.id,
    )
    if not is_daily_menu_rated:
        view = DailyMenuRateSuggestionView(daily_menu_id=daily_menu.id)
        await answer_view(message, view)
