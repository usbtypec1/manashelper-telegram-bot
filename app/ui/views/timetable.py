import datetime
from collections.abc import Iterable
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.filters.callback_data.timetable import (
    FacultyCallbackData,
    DepartmentCallbackData, CourseCallbackData,
    CourseSpecificWeekdayTimetableCallbackData,
)
from app.models.courses import (
    UserTrackingCourses, DepartmentCourses,
    WeekdayCourseTimetable,
)
from app.models.departments import FacultyDepartments
from app.models.faculties import Faculty
from app.ui.views.base import TextView


class CourseSpecificWeekdayTimetableView(TextView):

    def __init__(self, timetable: WeekdayCourseTimetable):
        self.__timetable = timetable

    def get_text(self) -> str:
        timezone = ZoneInfo("Asia/Bishkek")
        now = datetime.datetime.now(timezone)
        weekdays = ("понедельник", "вторник", "среду", "четверг", "пятницу")
        weekday_name = weekdays[self.__timetable.weekday - 1]
        lines: list[str] = [f"<b>Расписание на {weekday_name}:</b>"]
        if not self.__timetable.lessons:
            lines.append("Пар нет! 🎉")
            return "\n".join(lines)

        for period_lessons in self.__timetable.lessons:
            is_now = (
                period_lessons.starts_at <= now.time() <= period_lessons.ends_at
            )
            is_next = (
                period_lessons.starts_at <= (now + datetime.timedelta(
                minutes=45,
            )).time() <= period_lessons.ends_at
            )
            emoji_prefix = ""
            if is_now:
                emoji_prefix = "🔥 "
            elif is_next:
                emoji_prefix = "⏱️🐇 "
            period = f"{emoji_prefix}{period_lessons.starts_at:%H:%M} - {period_lessons.ends_at:%H:%M}"
            lines.append(f"\n<b>{period}</b>")
            prefix = "• " if len(period_lessons.lessons) > 1 else ""
            for lesson in period_lessons.lessons:
                lines.append(
                    f"<b>{prefix}{lesson.name}</b>\n"
                    f"  🏫 {lesson.location}",
                )
        return "\n".join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        timezone = ZoneInfo("Asia/Bishkek")
        builder = InlineKeyboardBuilder()
        for number, weekday in enumerate(
            ("Пн", "Вт", "Ср", "Чт", "Пт"),
            start=1,
        ):
            if number == self.__timetable.weekday:
                weekday = f"✅ {weekday}"
            builder.button(
                text=weekday,
                callback_data=CourseSpecificWeekdayTimetableCallbackData(
                    weekday=number,
                ),
            )

        builder.row(
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="timetable_menu",
            ),
        )
        return builder.adjust(5, repeat=True).as_markup()


class UserTrackingCourseListView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗓️ Посмотреть расписание",
                    callback_data="view_timetable",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Настроить отслеживание",
                    callback_data="edit_tracking_courses",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="main_menu",
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
