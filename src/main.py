import asyncio
import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from handlers.registry import get_routers
from setup.config.settings import load_settings_from_toml_file, AppSettings
from setup.ioc.registry import get_providers


async def setup_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(
                command="start",
                description="📲 Главное меню",
            ),
            BotCommand(
                command="yemek",
                description="🍽️ Посмотреть меню йемека",
            ),
            BotCommand(
                command="yoklama",
                description="🤚 Посмотреть посещаемость",
            ),
            BotCommand(
                command="exams",
                description="💯 Посмотреть баллы за экзамены",
            ),
            BotCommand(
                command="timetable",
                description="📅 Посмотреть расписание занятий",
            ),
            BotCommand(
                command="about",
                description="ℹ️ Информация о боте",
            ),
        ],
    )


async def main() -> None:
    settings = load_settings_from_toml_file()

    container = make_async_container(
        *get_providers(),
        context={AppSettings: settings},
    )

    bot = await container.get(Bot)
    dispatcher = await container.get(Dispatcher)
    dispatcher.include_routers(*get_routers())

    setup_dishka(router=dispatcher, container=container, auto_inject=True)

    await setup_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
