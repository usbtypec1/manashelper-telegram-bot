from aiogram import Router

from app.handlers.about import about_router
from app.handlers.attendance import attendance_router
from app.handlers.exams import exams_router
from app.handlers.food_menu import food_menu_router
from app.handlers.global_errors import global_errors_router
from app.handlers.obis_credentials import obis_credentials_router
from app.handlers.start import start_router
from app.handlers.timetable import timetable_router


def get_routers() -> tuple[Router, ...]:
    return (
        start_router,
        obis_credentials_router,
        attendance_router,
        exams_router,
        food_menu_router,
        timetable_router,
        about_router,
        global_errors_router,
    )
