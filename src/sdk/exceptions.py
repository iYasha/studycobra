from typing import List
from typing import NamedTuple
from typing import Optional

from fastapi.exceptions import RequestValidationError
from sso_auth.exceptions import SSOBaseAuthException
from pydantic import BaseModel
from sentry_sdk import capture_exception
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class FieldErrorModel(BaseModel):
    field: str
    message: str


class ExceptionModel(BaseModel):
    code: int = 400
    error_message: str
    field_errors: Optional[List[FieldErrorModel]]


def auth_exception_handler(request: Request, exc: SSOBaseAuthException) -> JSONResponse:
    capture_exception(exc)

    error_message = exc.detail

    response = ExceptionModel(error_message=error_message)
    return JSONResponse(response.dict(), status_code=exc.status_code)


def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    capture_exception(exc)

    error_message = str(exc)

    response = ExceptionModel(error_message=error_message)
    return JSONResponse(response.dict(), status_code=400)


class FieldError(NamedTuple):
    field: str
    message: str


class ValidationError(Exception):
    """Ошибка валидации."""

    DEFAULT_MESSAGE = "Ошибка валидации"

    def __init__(
        self, message: str = None, code: int = 400, field_errors: Optional[List[FieldError]] = None
    ) -> None:
        self.message = message or self.DEFAULT_MESSAGE
        self.code = code
        self.field_errors = field_errors


def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    field_errors = None

    if exc.field_errors:
        field_errors = [FieldError(field=fe.field, message=fe.message) for fe in exc.field_errors]

    content = ExceptionModel(
        code=exc.code,
        error_message=exc.message,
        field_errors=field_errors,
    )
    return JSONResponse(content.dict(), status_code=exc.code)


def fastapi_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    field_errors = [
        FieldErrorModel(field=str(error.get("loc", "")), message=error.get("msg", ""))
        for error in exc.errors()
    ]

    content = ExceptionModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message="Ошибка валидации параметров",
        field_errors=field_errors,
    )

    return JSONResponse(content.dict(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
