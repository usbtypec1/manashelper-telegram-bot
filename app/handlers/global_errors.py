from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent


global_errors_router = Router(name=__name__)


@global_errors_router.error(ExceptionTypeFilter(Exception))
async def on_global_exception(
    event: ErrorEvent,
) -> None:
    text = "❗️ Произошла ошибка. Информация отправлена разработчикам, скоро всё исправим! 😊"
    if event.update.message is not None:
        await event.update.message.answer(text)
    elif event.update.callback_query is not None:
        await event.update.callback_query.answer(text, show_alert=True)
