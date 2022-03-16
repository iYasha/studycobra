from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union

from pydantic import BaseModel


class FieldError(NamedTuple):
    field: str
    message: str


class FieldErrorModel(BaseModel):
    field: str
    message: str


class ExceptionModel(BaseModel):
    code: int = 400
    error_message: str
    field_errors: Optional[List[Union[FieldErrorModel, FieldError]]]
    service_code: Optional[str] = None
