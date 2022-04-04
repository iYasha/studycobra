from typing import List
from typing import Optional
from typing import Union

from exceptions.schemas import FieldError
from exceptions.schemas import FieldErrorModel

__all__ = ["BaseError", "ValidationError"]


class BaseError(Exception):
    """Базовый класс ошибок"""

    message: Optional[str]
    code: int
    field_errors: Optional[List[Union[FieldError, FieldErrorModel]]]

    def __init__(
        self,
        message: Optional[str] = None,
        code: int = 400,
        field_errors: Optional[List[Union[FieldError, FieldErrorModel]]] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.field_errors = field_errors


class ValidationError(BaseError):
    """Ошибки валидации бизнес-логики"""

    def __init__(
        self,
        message: Optional[str] = "Ошибка валидации",
        code: int = 400,
        field_errors: Optional[List[Union[FieldError, FieldErrorModel]]] = None,
    ) -> None:
        super().__init__(message, code, field_errors)


class NotFoundError(ValidationError):
    DEFAULT_MESSAGE = "Запись не найдена"
