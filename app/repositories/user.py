from pymongo import AsyncMongoClient

from app.models.attendance import LessonAttendance
from app.models.exam import LessonExams
from app.models.users import UsersStatistics, UserGetResponse


class UserRepository:

    def __init__(self, mongodb_client: AsyncMongoClient):
        self.__users = mongodb_client.users

    async def get_user_by_id(self, user_id: int) -> UserGetResponse:
        raise NotImplementedError

    async def upsert_user(
        self,
        user_id: int,
        full_name: str,
        username: str | None,
    ) -> None:
        await self.__users.update_one(
            {"chat_id", user_id},
            {"$set": {"full_name": full_name, "username": username}},
            upsert=True,
        )

    async def update_user_credentials(
        self,
        user_id: int,
        student_number: str,
        encrypted_password: str,
    ) -> None:
        await self.__users.update_one(
            {"chat_id", user_id},
            {"$set": {
                "student_number": student_number,
                "encrypted_password": encrypted_password,
            }},
            upsert=True,
        )

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
