from typing import Final

from models.attendance import (
    LessonAttendance,
    LessonAttendanceAndSkipsOpportunity,
)
from models.exam import LessonExams
from models.users import UsersStatistics
from repositories.user import UserRepository


THEORY_SKIPS_THRESHOLD: Final[int] = 30
PRACTICE_SKIPS_THRESHOLD: Final[int] = 20
SKIP_PERCENTAGE_PER_LESSON: Final[float] = 6.25


def compute_lesson_skip_opportunities(
    lesson: LessonAttendance,
) -> LessonAttendanceAndSkipsOpportunity:
    if lesson.theory_skips_percentage is not None:
        diff = (
            THEORY_SKIPS_THRESHOLD - lesson.theory_skips_percentage
        )
        if diff == SKIP_PERCENTAGE_PER_LESSON:
            theory_skippable_lessons_count = 0
        else:
            theory_skippable_lessons_count = int(
                diff // SKIP_PERCENTAGE_PER_LESSON,
            )
    else:
        theory_skippable_lessons_count = None
    if lesson.practice_skips_percentage is not None:
        diff = (
            PRACTICE_SKIPS_THRESHOLD
            - lesson.practice_skips_percentage
        )
        if diff == SKIP_PERCENTAGE_PER_LESSON:
            practice_skippable_lessons_count = 0
        else:
            practice_skippable_lessons_count = int(
                diff // SKIP_PERCENTAGE_PER_LESSON,
            )
    else:
        practice_skippable_lessons_count = None

    return LessonAttendanceAndSkipsOpportunity(
        lesson_name=lesson.lesson_name,
        lesson_code=lesson.lesson_code,
        theory_skips_percentage=lesson.theory_skips_percentage,
        practice_skips_percentage=lesson.practice_skips_percentage,
        theory_skips_opportunity=theory_skippable_lessons_count,
        practice_skips_opportunity=practice_skippable_lessons_count,
    )


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    async def update_user_credentials(
        self,
        user_id: int,
        student_number: str,
        plain_password: str,
    ) -> None:
        await self.__user_repository.update_user_credentials(
            user_id=user_id,
            student_number=student_number,
            plain_password=plain_password,
        )

    async def upsert_user(
        self,
        user_id: int,
        full_name: str,
        username: str | None,
    ) -> None:
        await self.__user_repository.upsert_user(
            user_id=user_id,
            full_name=full_name,
            username=username,
        )

    async def get_user_attendance(
        self,
        user_id: int,
    ) -> list[LessonAttendanceAndSkipsOpportunity]:
        lessons_attendance = await self.__user_repository.get_user_attendance(
            user_id=user_id,
        )
        return [
            compute_lesson_skip_opportunities(lesson)
            for lesson in lessons_attendance
        ]

    async def get_user_exams(
        self,
        user_id: int,
    ) -> list[LessonExams]:
        return await self.__user_repository.get_user_exams(user_id)

    async def get_users_statistics(self) -> UsersStatistics:
        return await self.__user_repository.get_users_statistics()
