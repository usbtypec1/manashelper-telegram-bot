from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka

from services.user import UserService
from ui.views.base import answer_view, edit_message_by_view
from ui.views.menu import MainMenuView, FoodMenuView, ObisMenuView


start_router = Router(name=__name__)


@start_router.message(CommandStart())
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


@start_router.callback_query(F.data == "main_menu")
async def on_main_menu_callback_query(
    callback_query: CallbackQuery,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.upsert_user(
        user_id=callback_query.from_user.id,
        full_name=callback_query.from_user.full_name,
        username=callback_query.from_user.username,
    )
    view = MainMenuView()
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer("")


@start_router.callback_query(F.data == "food_menu")
async def on_food_menu_command(callback_query: CallbackQuery) -> None:
    view = FoodMenuView()
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer("")


@start_router.callback_query(F.data == "obis_menu")
async def on_obis_menu_command(callback_query: CallbackQuery) -> None:
    view = ObisMenuView()
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer("")
