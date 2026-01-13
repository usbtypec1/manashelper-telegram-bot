from collections.abc import Iterable
from uuid import UUID

from pydantic import TypeAdapter

from models.courses import DepartmentCourses, UserTrackingCourses
from models.departments import FacultyDepartments
from models.faculties import Faculty
from repositories.error_handler import handle_api_errors
from repositories.http_client import ApiHttpClient


class TimetableRepository:

    def __init__(self, http_client: ApiHttpClient):
        self.__http_client = http_client

    async def get_faculties(self) -> list[Faculty]:
        url = "/timetable/faculties"
        response = await self.__http_client.get(url)
        type_adapter = TypeAdapter(list[Faculty])
        handle_api_errors(response)
        return type_adapter.validate_json(response.text)

    async def get_departments(self, faculty_id: UUID) -> FacultyDepartments:
        url = "/timetable/departments"
        params = {"facultyId": str(faculty_id)}
        response = await self.__http_client.get(url, params=params)
        handle_api_errors(response)
        return FacultyDepartments.model_validate_json(response.text)

    async def get_courses(self, department_id: UUID) -> DepartmentCourses:
        url = "/timetable/courses"
        params = {"departmentId": str(department_id)}
        response = await self.__http_client.get(url, params=params)
        handle_api_errors(response)
        return DepartmentCourses.model_validate_json(response.text)

    async def get_user_tracking_courses(
        self,
        user_id: int,
    ) -> UserTrackingCourses:
        url = f"/timetable/tracking/users/{user_id}"
        response = await self.__http_client.get(url)
        handle_api_errors(response)
        return UserTrackingCourses.model_validate_json(response.text)

    async def update_user_tracking_courses(
        self,
        user_id: int,
        course_ids: Iterable[int],
    ) -> None:
        url = f"/timetable/tracking/users/{user_id}"
        request_data = {"courseIds": tuple(course_ids)}
        response = await self.__http_client.put(url, json=request_data)
        handle_api_errors(response)
