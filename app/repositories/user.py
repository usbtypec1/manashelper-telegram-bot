from app.models.attendance import LessonAttendance
from app.models.exam import LessonExams
from app.models.users import UsersStatistics, UserGetResponse, UserUpdateRequest


class UserRepository:

    async def get_user_by_id(self, user_id: int) -> UserGetResponse:
        raise NotImplementedError

    async def update_user_by_id(
        self,
        *,
        user_id: int,
        request_data: UserUpdateRequest,
    ) -> None:
        raise NotImplementedError

    async def upsert_user(
        self,
        user_id: int,
        full_name: str,
        username: str | None,
    ) -> None:
        raise NotImplementedError

    async def update_user_credentials(
        self,
        user_id: int,
        student_number: str,
        plain_password: str,
    ) -> None:
        raise NotImplementedError

    async def get_user_attendance(
        self,
        user_id: int,
    ) -> list[LessonAttendance]:
        raise NotImplementedError

    async def get_user_exams(
        self,
        user_id: int,
    ) -> list[LessonExams]:
        raise NotImplementedError

    async def get_users_statistics(self) -> UsersStatistics:
        raise NotImplementedError
