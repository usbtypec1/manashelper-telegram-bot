from aiogram import Router

from app.handlers.food_menu import food_menu_router
from app.handlers.global_errors import global_errors_router
from app.handlers.start import start_router


def get_routers() -> tuple[Router, ...]:
    return (
        start_router,
        food_menu_router,
        global_errors_router,
    )
