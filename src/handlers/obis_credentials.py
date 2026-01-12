from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent
from dishka import FromDishka

from exceptions.users import UserHasNoCredentialsException
from models.user import UserCredentialsWebAppData
from services.user import UserService


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



@obis_credentials_router.message(
    F.web_app_data.button_text == "Ввести данные от OBIS",
)
async def on_obis_credentials_enter(
    message: Message,
    user_service: FromDishka[UserService],
) -> None:
    user_credentials = UserCredentialsWebAppData.model_validate_json(
        message.web_app_data.data,
    )
    await user_service.update_user_credentials(
        user_id=message.from_user.id,
        student_number=user_credentials.student_number,
        plain_password=user_credentials.plain_password.get_secret_value(),
    )
