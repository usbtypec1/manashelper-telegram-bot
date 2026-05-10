import datetime
from collections.abc import Iterable
from uuid import UUID

from aiogram.types import (
    InputMediaPhoto, InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.media_group import MediaType

from app.filters.callback_data.food_menu import (
    DailyMenuRatingCallbackData,
    DailyMenuCommentCallbackData, DailyMenuShowCommentsCallbackData,
)
from app.models.food_menu import DailyMenu, DailyMenuRating
from app.ui.views.base import MediaGroupView, TextView, ReplyMarkup


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
            InputMediaPhoto(media=item.upscaled_photo_url or item.photo_url)
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


class DailyMenuShowCommentsView(TextView):
    text = "💬 Посмотреть отзывы о сегодняшнем йемеке"

    def __init__(self, daily_menu_id: UUID) -> None:
        self.__daily_menu_id = daily_menu_id

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Посмотреть отзывы 💬",
                        callback_data=DailyMenuShowCommentsCallbackData(
                            daily_menu_id=self.__daily_menu_id,
                        ).pack(),
                    ),
                ]
            ],
        )


class DailyMenuCommentListView(TextView):
    def __init__(self, ratings: Iterable[DailyMenuRating]) -> None:
        self.__ratings = ratings

    def get_text(self) -> str:
        if not self.__ratings:
            return "Пока что нет отзывов о сегодняшнем йемеке. Станьте первым, кто оставит отзыв! 📝"

        lines: list[str] = ["💬 <b>Отзывы о сегодняшнем йемеке:</b>\n"]
        for rating in self.__ratings:
            lines.append(
                f"- {rating.user_full_name}: {rating.comment}"
                f" (⭐️ {rating.score:.1f})\n",
            )

        return "\n".join(lines)
