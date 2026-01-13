import httpx
from pydantic import ValidationError

from enums.api_error_code import ApiErrorCode
from exceptions.api import ApiErrorFormatException, ValidationException
from exceptions.users import (
    UserNotFoundException,
    UserHasNoCredentialsException, ObisLoginException,
)
from models.api import ApiError


API_ERROR_CODE_TO_EXCEPTION_CLASS = {
    ApiErrorCode.USER_NOT_FOUND: UserNotFoundException,
    ApiErrorCode.USER_HAS_NO_CREDENTIALS: UserHasNoCredentialsException,
    ApiErrorCode.OBIS_LOGIN_FAILED: ObisLoginException,
    ApiErrorCode.VALIDATION_FAILED: ValidationException,
}


def handle_api_errors(response: httpx.Response) -> None:
    if not response.is_error:
        return

    try:
        api_error = ApiError.model_validate_json(response.text)
    except ValidationError:
        raise ApiErrorFormatException("Invalid API error format")

    exception_class = API_ERROR_CODE_TO_EXCEPTION_CLASS.get(
        api_error.code,
        Exception,
    )
    raise exception_class(api_error.message)
