from collections.abc import Iterable
from uuid import UUID

from app.models.courses import (
    DepartmentCourses, UserTrackingCourses,
    CourseTimetableLesson,
)
from app.models.departments import FacultyDepartments
from app.models.faculties import Faculty


class TimetableRepository:

    async def get_course_timetable(
        self,
        course_ids: Iterable[int],
        weekday: int,
    ) -> list[CourseTimetableLesson]:
        raise NotImplementedError

    async def get_faculties(self) -> list[Faculty]:
        raise NotImplementedError

    async def get_departments(self, faculty_id: UUID) -> FacultyDepartments:
        raise NotImplementedError

    async def get_courses(self, department_id: UUID) -> DepartmentCourses:
        raise NotImplementedError

    async def get_user_tracking_courses(
        self,
        user_id: int,
    ) -> UserTrackingCourses:
        raise NotImplementedError

    async def update_user_tracking_courses(
        self,
        user_id: int,
        course_ids: Iterable[int],
    ) -> None:
        raise NotImplementedError
