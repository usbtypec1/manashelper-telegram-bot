import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from models.food_menu import DailyMenu, DailyMenuRating
from repositories.food_menu import FoodMenuRepository


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "")
        .replace("'", "")
    )


def remove_extra_spaces(text: str) -> str:
    return ' '.join(text.split())


def remove_newlines(text: str) -> str:
    return text.replace('\n', ' ').replace('\r', ' ')


def sanitize_comment(comment: str) -> str | None:
    sanitized = comment.strip()
    sanitizers = (
        remove_newlines,
        remove_extra_spaces,
        escape_html,
    )
    for sanitizer in sanitizers:
        sanitized = sanitizer(sanitized)
    return sanitized if sanitized else None


class FoodMenuService:

    def __init__(self, food_menu_repository: FoodMenuRepository):
        self.__food_menu_repository = food_menu_repository

    async def get_food_menu(
        self,
        *,
        days_to_skip: int,
    ) -> DailyMenu:
        timezone = ZoneInfo("Asia/Bishkek")
        date = datetime.datetime.now(timezone) + datetime.timedelta(
            days=days_to_skip,
        )
        return await self.__food_menu_repository.get_food_menu(date=date)

    async def is_daily_menu_rated_by_user(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
    ) -> bool:
        ratings = await self.__food_menu_repository.get_daily_menu_rating(
            daily_menu_id=daily_menu_id,
            user_id=user_id,
        )
        return len(ratings) > 0

    async def get_daily_menu_ratings_with_comments(
        self,
        daily_menu_id: UUID,
    ) -> list[DailyMenuRating]:
        ratings = await self.__food_menu_repository.get_daily_menu_rating(
            daily_menu_id=daily_menu_id,
        )
        return [
            rating for rating in ratings if rating.comment is not None
        ]

    async def update_daily_menu_rating(
        self,
        *,
        user_id: int,
        daily_menu_id: UUID,
        score: int,
        comment: str | None = None,
    ) -> None:
        comment = sanitize_comment(comment)
        await self.__food_menu_repository.update_daily_menu_rating(
            user_id=user_id,
            daily_menu_id=daily_menu_id,
            score=score,
            comment=comment,
        )
