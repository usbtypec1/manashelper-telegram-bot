from pydantic import BaseModel

from enums.api_error_code import ApiErrorCode


class ApiError(BaseModel):
    code: ApiErrorCode
    message: str
