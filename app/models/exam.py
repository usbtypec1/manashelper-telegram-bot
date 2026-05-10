from typing import Annotated

from pydantic import BaseModel, Field


class Exam(BaseModel):
    name: str
    score: str | None


class LessonExams(BaseModel):
    lesson_name: Annotated[str, Field(validation_alias="lessonName")]
    lesson_code: Annotated[str, Field(validation_alias="lessonCode")]
    exams: list[Exam]
