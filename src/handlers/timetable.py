from aiogram import Router, F
from aiogram.types import CallbackQuery
from dishka import FromDishka

from exceptions.api import ValidationException
from filters.callback_data.timetable import (
    FacultyCallbackData,
    DepartmentCallbackData, CourseCallbackData,
)
from services.timetable import TimetableService
from ui.views.base import edit_message_by_view
from ui.views.timetable import (
    UserTrackingCourseListView, FacultyListView,
    DepartmentListView, CourseListView,
)


timetable_router = Router(name=__name__)


@timetable_router.callback_query(F.data == "timetable_menu")
async def on_timetable_menu_callback_query(
    callback_query: CallbackQuery,
    timetable_service: FromDishka[TimetableService],
) -> None:
    user_tracking_courses = await timetable_service.get_user_tracking_courses(
        user_id=callback_query.from_user.id,
    )
    view = UserTrackingCourseListView(user_tracking_courses)
    await edit_message_by_view(callback_query.message, view)


@timetable_router.callback_query(F.data == "edit_tracking_courses")
async def on_edit_tracking_courses_callback_query(
    callback_query: CallbackQuery,
    timetable_service: FromDishka[TimetableService],
) -> None:
    faculties = await timetable_service.get_faculties()
    view = FacultyListView(faculties)
    await edit_message_by_view(callback_query.message, view)


@timetable_router.callback_query(FacultyCallbackData.filter())
async def on_faculty_callback_query(
    callback_query: CallbackQuery,
    callback_data: FacultyCallbackData,
    timetable_service: FromDishka[TimetableService],
) -> None:
    faculty_departments = await timetable_service.get_departments(
        faculty_id=callback_data.faculty_id,
    )
    view = DepartmentListView(faculty_departments)
    await edit_message_by_view(callback_query.message, view)


@timetable_router.callback_query(DepartmentCallbackData.filter())
async def on_department_callback_query(
    callback_query: CallbackQuery,
    callback_data: DepartmentCallbackData,
    timetable_service: FromDishka[TimetableService],
) -> None:
    department_courses = await timetable_service.get_courses(
        department_id=callback_data.department_id,
    )
    user_tracking_courses = await timetable_service.get_user_tracking_courses(
        user_id=callback_query.from_user.id,
    )
    view = CourseListView(
        department_courses=department_courses,
        user_tracking_courses=user_tracking_courses,
    )
    await edit_message_by_view(callback_query.message, view)


@timetable_router.callback_query(CourseCallbackData.filter())
async def on_course_callback_query(
    callback_query: CallbackQuery,
    callback_data: CourseCallbackData,
    timetable_service: FromDishka[TimetableService],
) -> None:
    department_courses = await timetable_service.get_courses(
        department_id=callback_data.department_id,
    )
    try:
        await timetable_service.toggle_user_tracking_course(
            user_id=callback_query.from_user.id,
            course_id=callback_data.course_id,
        )
    except ValidationException:
        await callback_query.answer(
            text="❌ Вы не можете отслеживать больше 5 курсов.",
            show_alert=True,
        )
        return

    user_tracking_courses = await timetable_service.get_user_tracking_courses(
        user_id=callback_query.from_user.id,
    )
    view = CourseListView(
        department_courses=department_courses,
        user_tracking_courses=user_tracking_courses,
    )
    await edit_message_by_view(callback_query.message, view)
