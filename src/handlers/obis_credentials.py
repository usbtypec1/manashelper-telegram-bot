from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ErrorEvent, CallbackQuery
from dishka import FromDishka

from exceptions.users import UserHasNoCredentialsException
from filters.states.obis_credentials import ObisCredentialsStates
from services.user import UserService
from ui.views.base import answer_view
from ui.views.menu import ObisMenuView


obis_credentials_router = Router(name=__name__)


@obis_credentials_router.error(
    ExceptionTypeFilter(UserHasNoCredentialsException),
)
async def on_user_has_no_credentials_exception(
    event: ErrorEvent,
) -> None:
    if event.update.message is not None:
        await event.update.message.answer("Пожалуйста, введите ваши данные от OBIS.")
    elif event.update.callback_query is not None:
        await event.update.callback_query.answer(
            "Пожалуйста, введите ваши данные от OBIS.",
            show_alert=True,
        )


@obis_credentials_router.callback_query(F.data == "obis_credentials")
async def on_obis_credentials_callback_query(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(ObisCredentialsStates.student_number)
    await callback_query.message.edit_text(
        "✏️ Введите ваш студенческий номер:",
    )
    await callback_query.answer("")


@obis_credentials_router.message(
    F.text,
    StateFilter(ObisCredentialsStates.student_number),
)
async def on_student_number_enter(
    message: Message,
    state: FSMContext,
) -> None:
    student_number = message.text.removesuffix("@manas.edu.kg")
    await state.update_data(student_number=student_number)
    await state.set_state(ObisCredentialsStates.password)
    await message.answer("✏️ Введите ваш пароль от OBIS:")


@obis_credentials_router.message(
    F.text,
    StateFilter(ObisCredentialsStates.password),
)
async def on_password_enter(
    message: Message,
    state: FSMContext,
    user_service: FromDishka[UserService],
) -> None:
    data = await state.get_data()
    student_number = data["student_number"]
    plain_password = message.text

    await user_service.update_user_credentials(
        user_id=message.from_user.id,
        student_number=student_number,
        plain_password=plain_password,
    )
    await state.clear()
    await message.answer("✅ Ваши данные от OBIS успешно сохранены.")
    view = ObisMenuView()
    await answer_view(message, view)
