import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class Dish(BaseModel):
    name: str
    calories: int
    photo_url: Annotated[str, Field(validation_alias="photoUrl")]


class DailyMenu(BaseModel):
    dishes: list[Dish]
    date: datetime.date
