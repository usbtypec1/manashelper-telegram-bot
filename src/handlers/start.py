from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message
from dishka import FromDishka

from services.user import UserService
from ui.views.base import answer_view
from ui.views.menu import MainMenuView, FoodMenuView, ObisMenuView


start_router = Router(name=__name__)


@start_router.message(
    or_f(
        CommandStart(),
        F.text == "Назад",
    ),
)
async def on_start_command(
    message: Message,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.upsert_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )
    view = MainMenuView()
    await answer_view(message, view)


@start_router.message(F.text == "Йемек")
async def on_food_menu_command(message: Message) -> None:
    view = FoodMenuView()
    await answer_view(message, view)


@start_router.message(F.text == "OBIS")
async def on_obis_menu_command(message: Message) -> None:
    view = ObisMenuView()
    await answer_view(message, view)
