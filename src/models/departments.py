from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Department(BaseModel):
    id: UUID
    name: str


class FacultyDepartments(BaseModel):
    faculty_id: Annotated[UUID, Field(validation_alias="facultyId")]
    faculty_name: Annotated[str, Field(validation_alias="facultyName")]
    departments: list[Department]
