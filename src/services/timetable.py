from uuid import UUID

from models.courses import UserTrackingCourses, DepartmentCourses
from models.departments import FacultyDepartments
from models.faculties import Faculty
from repositories.timetable import TimetableRepository


class TimetableService:

    def __init__(self, timetable_repository: TimetableRepository):
        self.__timetable_repository = timetable_repository

    async def get_user_tracking_courses(
        self,
        user_id: int,
    ) -> UserTrackingCourses:
        return await self.__timetable_repository.get_user_tracking_courses(
            user_id=user_id,
        )

    async def toggle_user_tracking_course(
        self,
        user_id: int,
        course_id: int,
    ) -> None:
        user_tracking_courses = await self.get_user_tracking_courses(user_id)
        course_ids = {course.id for course in user_tracking_courses.courses}
        if course_id in course_ids:
            course_ids.remove(course_id)
        else:
            course_ids.add(course_id)
        await self.__timetable_repository.update_user_tracking_courses(
            user_id=user_id,
            course_ids=course_ids,
        )

    async def get_faculties(self) -> list[Faculty]:
        return await self.__timetable_repository.get_faculties()

    async def get_departments(self, faculty_id: UUID) -> FacultyDepartments:
        return await self.__timetable_repository.get_departments(faculty_id)

    async def get_courses(self, department_id: UUID) -> DepartmentCourses:
        return await self.__timetable_repository.get_courses(department_id)
