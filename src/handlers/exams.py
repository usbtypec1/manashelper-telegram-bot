from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from dishka import FromDishka

from services.user import UserService
from ui.views.base import edit_message_by_view, answer_view
from ui.views.exams import UserExamsView


exams_router = Router(name=__name__)


@exams_router.message(Command("exams"))
async def on_exams_command(
    message: Message,
    user_service: FromDishka[UserService],
) -> None:
    pending_message = await message.answer(text="Загрузка...")
    lessons_exams = await user_service.get_user_exams(message.from_user.id)
    view = UserExamsView(lessons_exams=lessons_exams)
    await edit_message_by_view(pending_message, view)


@exams_router.callback_query(F.data == "exams")
async def on_exams_callback_query(
    callback_query: Message,
    user_service: FromDishka[UserService],
) -> None:
    lessons_exams = await user_service.get_user_exams(
        user_id=callback_query.from_user.id,
    )
    view = UserExamsView(lessons_exams=lessons_exams)
    await answer_view(callback_query.message, view)
    await callback_query.answer("")
