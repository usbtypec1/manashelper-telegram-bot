import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class Dish(BaseModel):
    name: str
    calories: int
    photo_url: Annotated[str, Field(validation_alias="photoUrl")]


class DailyMenu(BaseModel):
    id: UUID
    dishes: list[Dish]
    date: datetime.date
    average_rating_score: Annotated[float, Field(alias="averageRatingScore")]
    ratings_count: Annotated[int, Field(alias="ratingsCount")]


class DailyMenuRating(BaseModel):
    score: float
