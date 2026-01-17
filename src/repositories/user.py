from pydantic import TypeAdapter

from models.attendance import LessonAttendance
from models.exam import LessonExams
from models.users import UsersStatistics
from repositories.error_handler import handle_api_errors
from repositories.http_client import ApiHttpClient


class UserRepository:

    def __init__(self, http_client: ApiHttpClient):
        self.__http_client = http_client

    async def upsert_user(
        self,
        user_id: int,
        full_name: str,
        username: str | None,
    ) -> None:
        url = "/users"
        request_data = {
            "id": user_id,
            "fullName": full_name,
            "username": username,
        }
        response = await self.__http_client.post(url, json=request_data)
        handle_api_errors(response)

    async def update_user_credentials(
        self,
        user_id: int,
        student_number: str,
        plain_password: str,
    ) -> None:
        url = f"/users/{user_id}/credentials"
        request_data = {
            "studentNumber": student_number,
            "plainPassword": plain_password,
        }
        response = await self.__http_client.put(url, json=request_data)
        handle_api_errors(response)

    async def get_user_attendance(
        self,
        user_id: int,
    ) -> list[LessonAttendance]:
        url = f"/users/{user_id}/attendance"
        response = await self.__http_client.get(url)
        handle_api_errors(response)
        type_adapter = TypeAdapter(list[LessonAttendance])
        return type_adapter.validate_json(response.text)

    async def get_user_exams(
        self,
        user_id: int,
    ) -> list[LessonExams]:
        url = f"/users/{user_id}/exams"
        response = await self.__http_client.get(url)
        handle_api_errors(response)
        type_adapter = TypeAdapter(list[LessonExams])
        return type_adapter.validate_json(response.text)

    async def get_users_statistics(self) -> UsersStatistics:
        url = "/users/statistics"
        response = await self.__http_client.get(url)
        handle_api_errors(response)
        return UsersStatistics.model_validate_json(response.text)
