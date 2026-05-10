from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka

from services.user import UserService
from ui.views.about import (
    AboutView,
    AboutWhyCredentialsView,
    AboutHowItWorksView,
    AboutDeveloperView,
)
from ui.views.base import answer_view, edit_message_by_view


about_router = Router(name=__name__)


@about_router.message(Command("about"))
async def on_about_command(message: Message) -> None:
    view = AboutView()
    await answer_view(message, view)


@about_router.callback_query(F.data == "about")
async def on_about_callback_query(callback_query: CallbackQuery) -> None:
    view = AboutView()
    await edit_message_by_view(callback_query.message, view)


@about_router.callback_query(F.data == "about:why_credentials")
async def on_about_why_credentials_callback_query(
    callback_query: CallbackQuery,
    user_service: FromDishka[UserService],
) -> None:
    users_statistics = await user_service.get_users_statistics()
    view = AboutWhyCredentialsView(users_statistics)
    await edit_message_by_view(callback_query.message, view)


@about_router.callback_query(F.data == "about:how_it_works")
async def on_about_how_it_works_callback_query(
    callback_query: CallbackQuery,
) -> None:
    view = AboutHowItWorksView()
    await edit_message_by_view(callback_query.message, view)


@about_router.callback_query(F.data == "about:developer")
async def on_about_developer_callback_query(
    callback_query: CallbackQuery,
) -> None:
    view = AboutDeveloperView()
    await edit_message_by_view(callback_query.message, view)
