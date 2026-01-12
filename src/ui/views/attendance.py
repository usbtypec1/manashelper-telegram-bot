from collections.abc import Iterable
from typing import override

from models.attendance import LessonAttendanceAndSkipsOpportunity
from ui.views.base import TextView


def inflect_word_skips(count: int) -> str:
    count = abs(count)

    if count % 10 == 1 and count % 100 != 11:
        return "пропуск"
    elif count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return "пропуска"
    return "пропусков"


def format_float(value: float | None) -> str:
    if value is None:
        return "-"
    value = str(value)
    return value.rstrip("0").rstrip(".")


class UserAttendanceView(TextView):

    def __init__(
        self,
        lessons_attendance: Iterable[LessonAttendanceAndSkipsOpportunity],
    ) -> None:
        self.__lessons_attendance = lessons_attendance

    @override
    def get_text(self) -> str:
        lines: list[str] = []
        for lesson_attendance in self.__lessons_attendance:
            lesson_name = f"<b>{lesson_attendance.lesson_name}</b>"

            theory_skips = lesson_attendance.theory_skips_opportunity
            practice_skips = lesson_attendance.practice_skips_opportunity

            if practice_skips <= 1 or theory_skips <= 1:
                lesson_name = f"⚠️ {lesson_name}"
            elif practice_skips == 0 or theory_skips == 0:
                lesson_name = f"❗ {lesson_name}"

            lines.append(
                f"{lesson_name}\n"
                f"Теория: {format_float(lesson_attendance.theory_skips_percentage)}% (осталось {theory_skips} {inflect_word_skips(theory_skips)}\n"
                f"Практика: {format_float(lesson_attendance.practice_skips_percentage)}% (осталось {practice_skips} {inflect_word_skips(practice_skips)})",
            )

        if not lines:
            return "У вас нет предметов."
        return "\n\n".join(lines)
