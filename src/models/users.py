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
