from typing import List

from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.exceptions import ValidationError
from exceptions.helpers import classify_exception_and_send_to_sentry
from exceptions.helpers import load_error_translations
from exceptions.schemas import ExceptionModel
from exceptions.schemas import FieldErrorModel
from exceptions.translation import PydanticErrorTranslator
from exceptions.translation import pattern_translator_groupings
from sso_auth.exceptions import SSOBaseAuthException

tr = PydanticErrorTranslator(
    error_translations=load_error_translations(),
    pattern_translator_groupings=pattern_translator_groupings,
)


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Обработчик ошибок валидации параметров запроса - ошибки от Pydantic"""
    service_code = request.app.service_code
    field_errors: List[FieldErrorModel] = []

    for error in tr.translate(exc.errors()):
        field = list(error.get("loc", ""))

        if "body" in field:
            field.remove("body")

        field = ", ".join(field)
        message = error.get("msg", "")
        field_errors.append(FieldErrorModel(field=field, message=message))

    content = ExceptionModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message="Ошибка валидации параметров",
        field_errors=field_errors,
        service_code=service_code,
    )
    return JSONResponse(content.dict(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def logic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Обработчик ошибок валидации бизнес-логики"""

    service_code = request.app.service_code
    if exc.field_errors:
        field_errors = [
            FieldErrorModel(field=fe.field, message=fe.message) for fe in exc.field_errors
        ]  # noqa: C408,E501

    else:
        field_errors = []

    content = ExceptionModel(
        code=exc.code,
        error_message=exc.message,
        field_errors=field_errors,
        service_code=service_code,
    )

    return JSONResponse(content.dict(), status_code=exc.code)


def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Обработчик 404 ошибки"""
    service_code = request.app.service_code

    error_message = "Страница не найдена."
    if hasattr(exc, "detail") and exc.detail and exc.detail != "Not Found":
        error_message = exc.detail

    content = ExceptionModel(
        code=404,
        error_message=error_message,
        field_errors=[],
        service_code=service_code,
    )

    return JSONResponse(content.dict(), status_code=404)


def auth_exception_handler(request: Request, exc: SSOBaseAuthException) -> JSONResponse:
    """Обработчик ошибок аутентификации"""
    service_code = request.app.service_code
    content = ExceptionModel(error_message=exc.detail, service_code=service_code)
    return JSONResponse(content.dict(), status_code=exc.status_code)


def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Обработчик любых непредвиденных и необработанных ошибок"""
    service_code = request.app.service_code
    classify_exception_and_send_to_sentry(exc)
    error_message = "Возникла непредвиденная ошибка. Пожалуйста, обратитесь к администратору."
    content = ExceptionModel(error_message=error_message, service_code=service_code)

    return JSONResponse(content.dict(), status_code=400)
