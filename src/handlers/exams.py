from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message
from dishka import FromDishka

from services.user import UserService
from ui.views.base import edit_message_by_view
from ui.views.exams import UserExamsView


exams_router = Router(name=__name__)


@exams_router.message(
    or_f(
        F.text == "Экзамены",
        Command("exams"),
    ),
)
async def on_exams_command(
    message: Message,
    user_service: FromDishka[UserService],
) -> None:
    pending_message = await message.answer(text="Загрузка...")
    lessons_exams = await user_service.get_user_exams(message.from_user.id)
    view = UserExamsView(lessons_exams=lessons_exams)
    await edit_message_by_view(pending_message, view)

