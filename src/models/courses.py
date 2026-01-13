from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Course(BaseModel):
    id: int
    number: int


class DepartmentCourses(BaseModel):
    department_id: Annotated[UUID, Field(validation_alias="departmentId")]
    department_name: Annotated[str, Field(validation_alias="departmentName")]
    faculty_id: Annotated[UUID, Field(validation_alias="facultyId")]
    faculty_name: Annotated[str, Field(validation_alias="facultyName")]
    courses: list[Course]


class TrackingCourse(BaseModel):
    id: int
    number: int
    department_name: Annotated[str, Field(validation_alias="departmentName")]


class UserTrackingCourses(BaseModel):
    user_id: Annotated[int, Field(validation_alias="userId")]
    courses: list[TrackingCourse]
