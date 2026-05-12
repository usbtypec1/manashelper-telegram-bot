from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.exceptions.food_menu import DailyMenuNotFoundException
from app.filters.callback_data.food_menu import (
    FoodMenuCallbackData,
)
from app.services.food_menu import FoodMenuService
from app.ui.views.base import (
    answer_media_group_view,
    answer_view,
)
from app.ui.views.food_menu import DailyMenuView
from app.ui.views.menu import FoodMenuView


food_menu_router = Router(name=__name__)


@food_menu_router.callback_query(FoodMenuCallbackData.filter())
@inject
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


@food_menu_router.message(Command("yemek"))
@inject
async def on_food_menu_command(
    message: Message,
    command: CommandObject,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    if not command.args:
        view = FoodMenuView()
        await answer_view(message, view)
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
