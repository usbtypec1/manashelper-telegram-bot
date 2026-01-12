from collections.abc import Iterable

from models.exam import LessonExams
from ui.views.base import TextView


def format_none(value: str | None) -> str:
    return value if value is not None else "-"


class UserExamsView(TextView):

    def __init__(self, lessons_exams: Iterable[LessonExams]) -> None:
        self.__lessons_exams = lessons_exams

    def get_text(self) -> str:
        lines: list[str] = []
        for lesson_exams in self.__lessons_exams:
            lesson_lines = [
                f"<b>{lesson_exams.lesson_name} ({lesson_exams.lesson_code})</b>"]
            for exam in lesson_exams.exams:
                lesson_lines.append(
                    f" - {exam.name}: {format_none(exam.score)}",
                )
            lines.append("\n".join(lesson_lines))

        if not lines:
            return "У вас нет оценок за экзамены."
        return "\n\n".join(lines)
