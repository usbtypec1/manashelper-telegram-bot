from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message
from dishka import FromDishka

from services.user import UserService
from ui.views.attendance import UserAttendanceView
from ui.views.base import edit_message_by_view


attendance_router = Router(name=__name__)


@attendance_router.message(
    or_f(
        F.text == "Йоклама",
        Command("yoklama"),
    ),
)
async def on_attendance_command(
    message: Message,
    user_service: FromDishka[UserService],
) -> None:
    pending_message = await message.answer(text="Загрузка...")
    lessons_attendance = await user_service.get_user_attendance(
        user_id=message.from_user.id,
    )
    view = UserAttendanceView(lessons_attendance=lessons_attendance)
    await edit_message_by_view(pending_message, view)
