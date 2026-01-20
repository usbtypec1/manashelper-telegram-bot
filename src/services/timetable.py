import datetime
from collections import defaultdict
from uuid import UUID
from zoneinfo import ZoneInfo

from models.courses import (
    UserTrackingCourses, DepartmentCourses,
    WeekdayCoursePeriodLesson, WeekdayCoursePeriodLessons,
    WeekdayCourseTimetable,
)
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

    async def get_course_timetable_by_weekday(
        self,
        user_id: int,
        weekday: int,
    ) -> WeekdayCourseTimetable:
        tracking = await self.__timetable_repository.get_user_tracking_courses(user_id)
        lessons = await self.__timetable_repository.get_course_timetable(
            course_ids=[course.id for course in tracking.courses],
            weekday=weekday,
        )

        period_map: defaultdict = defaultdict(list)
        for lesson in lessons:
            period = (lesson.starts_at, lesson.ends_at)
            period_map[period].append(
                WeekdayCoursePeriodLesson(
                    name=lesson.name,
                    teacher_name=lesson.teacher_name,
                    location=lesson.location,
                    type=lesson.type,
                )
            )

        sorted_periods = sorted(period_map.keys(), key=lambda p: (p[0], p[1]))

        period_blocks = [
            WeekdayCoursePeriodLessons(
                starts_at=start,
                ends_at=end,
                lessons=period_map[(start, end)],
            )
            for (start, end) in sorted_periods
        ]

        return WeekdayCourseTimetable(
            weekday=weekday,
            lessons=period_blocks,
        )

    async def get_timetable_for_today(
        self,
        *,
        user_id: int,
    ) -> WeekdayCourseTimetable:
        timezone = ZoneInfo("Asia/Bishkek")
        today = datetime.datetime.now(timezone)
        return await self.get_course_timetable_by_weekday(
            user_id=user_id, 
            weekday=today.isoweekday(),
        )
