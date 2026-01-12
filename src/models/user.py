from typing import Annotated

from pydantic import BaseModel, Field, SecretStr


class UserCredentialsWebAppData(BaseModel):
    student_number: Annotated[
        str,
        Field(validation_alias="studentNumber"),
    ]
    plain_password: Annotated[
        SecretStr,
        Field(validation_alias="plainPassword"),
    ]
