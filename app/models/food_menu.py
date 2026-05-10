import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Dish(BaseModel):
    name: str
    calories: int
    photo_url: Annotated[str, Field(validation_alias="photoUrl")]
    upscaled_photo_url: Annotated[
        str | None,
        Field(validation_alias="upscaledPhotoUrl"),
    ]


class DailyMenu(BaseModel):
    id: UUID
    dishes: list[Dish]
    date: datetime.date
    average_rating_score: Annotated[float, Field(alias="averageRatingScore")]
    ratings_count: Annotated[int, Field(alias="ratingsCount")]
    has_comments: Annotated[bool, Field(alias="hasComments")]


class DailyMenuRating(BaseModel):
    user_id: Annotated[int, Field(alias="userId")]
    user_full_name: Annotated[str, Field(alias="userFullName")]
    score: float
    comment: str | None
