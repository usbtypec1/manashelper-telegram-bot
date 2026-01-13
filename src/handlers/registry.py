from aiogram import Router

from handlers.attendance import attendance_router
from handlers.exams import exams_router
from handlers.food_menu import food_menu_router
from handlers.obis_credentials import obis_credentials_router
from handlers.start import start_router
from handlers.timetable import timetable_router


def get_routers() -> tuple[Router, ...]:
    return (
        start_router,
        obis_credentials_router,
        attendance_router,
        exams_router,
        food_menu_router,
        timetable_router,
    )
