from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_data.timetable import (
    FacultyCallbackData,
    DepartmentCallbackData, CourseCallbackData,
)
from models.courses import UserTrackingCourses, DepartmentCourses
from models.departments import FacultyDepartments
from models.faculties import Faculty
from ui.views.base import TextView


class UserTrackingCourseListView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚙️ Настроить отслеживание",
                    callback_data="edit_tracking_courses",
                ),
            ],
        ],
    )

    def __init__(self, user_tracking_courses: UserTrackingCourses) -> None:
        self.__user_tracking_courses = user_tracking_courses

    def get_text(self) -> str:
        if not self.__user_tracking_courses.courses:
            return (
                "В этом разделе вы можете отслеживать изменение расписания."
            )
        lines: list[str] = ["<b>🗓️ Ваши отслеживаемые курсы:</b>"]
        for course in self.__user_tracking_courses.courses:
            lines.append(f"- {course.department_name} - {course.number} курс")
        return "\n".join(lines)


class FacultyListView(TextView):
    text = "Список факультетов:"

    def __init__(self, faculties: Iterable[Faculty]):
        self.__faculties = faculties

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for faculty in self.__faculties:
            builder.button(
                text=faculty.name,
                callback_data=FacultyCallbackData(faculty_id=faculty.id),
            )
        builder.button(text="🔙 Назад", callback_data="timetable_menu")
        return builder.adjust(1, repeat=True).as_markup()


class DepartmentListView(TextView):

    def __init__(self, faculty_departments: FacultyDepartments):
        self.__faculty_departments = faculty_departments

    def get_text(self) -> str:
        return f"<b>{self.__faculty_departments.faculty_name}</b>"

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for department in self.__faculty_departments.departments:
            builder.button(
                text=department.name,
                callback_data=DepartmentCallbackData(
                    department_id=department.id,
                ),
            )
        builder.button(
            text="🔙 Назад",
            callback_data="edit_tracking_courses",
        )
        return builder.adjust(1, repeat=True).as_markup()


class CourseListView(TextView):

    def __init__(
        self,
        department_courses: DepartmentCourses,
        user_tracking_courses: UserTrackingCourses,
    ):
        self.__department_courses = department_courses
        self.__user_tracking_courses = user_tracking_courses

    def get_text(self) -> str:
        return (
            f"<b>{self.__department_courses.faculty_name}"
            f" / {self.__department_courses.department_name}</b>"
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        tracked_course_ids = {
            course.id for course in self.__user_tracking_courses.courses
        }

        builder = InlineKeyboardBuilder()
        for course in self.__department_courses.courses:
            icon = "✅ " if course.id in tracked_course_ids else ""
            text = f"{icon}{course.number} курс"
            builder.button(
                text=text,
                callback_data=CourseCallbackData(
                    course_id=course.id,
                    department_id=self.__department_courses.department_id,
                ),
            )
        builder.button(
            text="🔙 Назад",
            callback_data=FacultyCallbackData(
                faculty_id=self.__department_courses.faculty_id,
            ),
        )
        return builder.adjust(1, repeat=True).as_markup()
