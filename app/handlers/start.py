from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dishka.integrations.aiogram import inject

from app.ui.views.base import answer_view, edit_message_by_view
from app.ui.views.menu import FoodMenuView


start_router = Router(name=__name__)


@start_router.message(CommandStart())
@inject
async def on_start_command(
    message: Message,
) -> None:
    view = FoodMenuView()
    await answer_view(message, view)


@start_router.callback_query(F.data == "main_menu")
@inject
async def on_main_menu_callback_query(
    callback_query: CallbackQuery,
) -> None:
    view = FoodMenuView()
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer("")
