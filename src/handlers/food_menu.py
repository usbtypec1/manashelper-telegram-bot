from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka

from filters.callback_data.food_menu import FoodMenuCallbackData
from services.food_menu import FoodMenuService
from ui.views.base import answer_media_group_view
from ui.views.food_menu import DailyMenuView


food_menu_router = Router(name=__name__)


@food_menu_router.callback_query(FoodMenuCallbackData.filter())
async def on_food_menu_callback_query(
    callback_query: CallbackQuery,
    callback_data: FoodMenuCallbackData,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    daily_menu = await food_menu_service.get_food_menu(
        days_to_skip=callback_data.days_to_skip,
    )

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=callback_query.message, view=view)
    await callback_query.answer("")


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

    daily_menu = await food_menu_service.get_food_menu(
        days_to_skip=days_to_skip,
    )

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=message, view=view)
