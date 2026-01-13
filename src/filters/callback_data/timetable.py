from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class FacultyCallbackData(CallbackData, prefix="faculty"):
    faculty_id: UUID


class DepartmentCallbackData(CallbackData, prefix="department"):
    department_id: UUID


class CourseCallbackData(CallbackData, prefix="course"):
    course_id: int
    department_id: UUID
