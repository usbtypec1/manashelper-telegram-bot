import asyncio
import sys
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Update
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from fastapi import FastAPI, Request, Response, status

from app.handlers.registry import get_routers
from app.setup.config.settings import load_settings, AppSettings
from app.setup.ioc.registry import get_providers


settings = load_settings()
bot = Bot(
    token=settings.telegram_bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dispatcher = Dispatcher(storage=MemoryStorage())


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        container = make_async_container(
            *get_providers(),
            context={AppSettings: settings},
        )
        dispatcher.include_routers(*get_routers())

        # autoinject does not work when feed_update used manually
        setup_dishka(router=dispatcher, container=container)

        await bot.set_webhook(url=settings.telegram_bot.webhook_url)
    except Exception as exc:
        pass
    yield
    await bot.close()

app = FastAPI(title="Manashelper", lifespan=lifespan)


@app.get("/")
async def index(request: Request):
    return "<h1>Hello</h1>"


@app.post("/")
async def on_update(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dispatcher.feed_update(bot, update)
    return Response(status_code=status.HTTP_200_OK)


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


if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    uvicorn.run("app:main:app", host="0.0.0.0", port=8000, reload=True)
