import datetime
from uuid import UUID

from aiogram.types import (
    InputMediaPhoto, InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.media_group import MediaType

from filters.callback_data.food_menu import (
    DailyMenuRatingCallbackData,
    DailyMenuCommentCallbackData,
)
from models.food_menu import DailyMenu
from ui.views.base import MediaGroupView, TextView, ReplyMarkup


def get_weekday_name(date: datetime.date) -> str:
    weekdays = (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
    )
    return weekdays[date.weekday()]


def inflate_word_rating(count: int) -> str:
    if 11 <= (count % 100) <= 14:
        return "оценок"
    last_digit = count % 10
    if last_digit == 1:
        return "оценка"
    if 2 <= last_digit <= 4:
        return "оценки"
    return "оценок"


class DailyMenuView(MediaGroupView):
    def __init__(self, daily_menu: DailyMenu) -> None:
        self.__daily_menu = daily_menu

    def get_medias(self) -> list[MediaType]:
        return [
            InputMediaPhoto(media=item.photo_url)
            for item in self.__daily_menu.dishes
        ]

    def get_caption(self) -> str:
        weekday_name = get_weekday_name(self.__daily_menu.date)
        lines: list[str] = [
            f"<b>🍽️ Меню на {self.__daily_menu.date:%d.%m.%Y} ({weekday_name}) 🍽️</b>"
        ]
        for dish in self.__daily_menu.dishes:
            lines.append(f"\n🧂 <u>{dish.name}</u>")
            lines.append(f"🌱 Калории: {dish.calories}")

        total_calories = sum(
            [dish.calories for dish in self.__daily_menu.dishes],
        )

        lines.append(f"\n🔥 <b>Сумма калорий: {total_calories}</b>")

        if self.__daily_menu.ratings_count:
            lines.append(
                "⭐ Сегодняшняя средняя оценка:"
                f" {self.__daily_menu.average_rating_score:.1f} "
                f"({self.__daily_menu.ratings_count}"
                f" {inflate_word_rating(self.__daily_menu.ratings_count)})",
            )

        return "\n".join(lines)


class DailyMenuRateSuggestionView(TextView):
    text = "🍽️ Как вам сегодняшний йемек? Оцените его!"

    def __init__(self, daily_menu_id: UUID) -> None:
        self.__daily_menu_id = daily_menu_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=str(score),
                        callback_data=DailyMenuRatingCallbackData(
                            daily_menu_id=self.__daily_menu_id,
                            score=score,
                        ).pack(),
                    )
                    for score in range(1, 6)
                ]
            ],
        )


class DailyMenuRatedView(TextView):

    def __init__(self, daily_menu_id: UUID, score: int) -> None:
        self.__daily_menu_id = daily_menu_id
        self.__score = score

    def get_text(self) -> str:
        return f"Вы поставили оценку {self.__score} ⭐️"

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Оставить комментарий 📝",
                        callback_data=DailyMenuCommentCallbackData(
                            daily_menu_id=self.__daily_menu_id,
                            score=self.__score,
                        ).pack(),
                    ),
                ],
            ],
        )
