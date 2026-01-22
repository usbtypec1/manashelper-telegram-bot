from typing import Annotated

from pydantic import BaseModel, Field


class UsersStatistics(BaseModel):
    total_users_count: Annotated[
        int,
        Field(validation_alias="totalUsersCount"),
    ]
    users_with_credentials_count: Annotated[
        int,
        Field(validation_alias="usersWithCredentialsCount"),
    ]


class UserGetResponse(BaseModel):
    id: int
    full_name: Annotated[
        str,
        Field(validation_alias="fullName"),
    ]
    username: str | None
    is_timetable_change_notifications_enabled: Annotated[
        bool,
        Field(validation_alias="isTimetableChangeNotificationsEnabled"),
    ]
    is_noon_food_menu_notifications_enabled: Annotated[
        bool,
        Field(validation_alias="isNoonFoodMenuNotificationsEnabled"),
    ]
    is_evening_food_menu_notifications_enabled: Annotated[
        bool,
        Field(validation_alias="isEveningFoodMenuNotificationsEnabled"),
    ]


class UserUpdateRequest(BaseModel):
    is_timetable_change_notifications_enabled: Annotated[
        bool,
        Field(serialization_alias="isTimetableChangeNotificationsEnabled"),
    ]
    is_noon_food_menu_notifications_enabled: Annotated[
        bool,
        Field(serialization_alias="isNoonFoodMenuNotificationsEnabled"),
    ]
    is_evening_food_menu_notifications_enabled: Annotated[
        bool,
        Field(serialization_alias="isEveningFoodMenuNotificationsEnabled"),
    ]
