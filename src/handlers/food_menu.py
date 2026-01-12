from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from services.food_menu import FoodMenuService
from ui.views.base import answer_media_group_view
from ui.views.food_menu import DailyMenuView


food_menu_router = Router(name=__name__)


@food_menu_router.message(
    F.text.in_(("🕕 Сегодня", "🕒 Завтра", "🕞 Послезавтра")),
)
async def on_food_menu_button(
    message: Message,
    food_menu_service: FromDishka[FoodMenuService],
) -> None:
    word_to_days_count = {
        "🕕 Сегодня": 0,
        "🕒 Завтра": 1,
        "🕞 Послезавтра": 2,
    }
    days_to_skip: int = word_to_days_count[message.text]

    daily_menu_list = await food_menu_service.get_food_menu()

    try:
        daily_menu = daily_menu_list[days_to_skip]
    except IndexError:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=message, view=view)


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

    daily_menu_list = await food_menu_service.get_food_menu()

    try:
        daily_menu = daily_menu_list[days_to_skip]
    except IndexError:
        await message.reply("Нет данных за указанный день 😔")
        return

    view = DailyMenuView(daily_menu)
    await answer_media_group_view(message=message, view=view)
