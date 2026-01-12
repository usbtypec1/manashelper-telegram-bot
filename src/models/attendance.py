from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class LessonAttendance(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    lesson_name: Annotated[str, Field(validation_alias="lessonName")]
    lesson_code: Annotated[str, Field(validation_alias="lessonCode")]
    theory_skips_percentage: Annotated[
        float | None,
        Field(validation_alias="theorySkipsPercentage"),
    ]
    practice_skips_percentage: Annotated[
        float | None,
        Field(validation_alias="practiceSkipsPercentage"),
    ]


class LessonAttendanceAndSkipsOpportunity(LessonAttendance):
    theory_skips_opportunity: int
    practice_skips_opportunity: int
