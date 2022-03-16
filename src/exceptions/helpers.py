import json
import re
from pathlib import Path
from typing import Dict

import sentry_sdk
from asyncpg import PostgresError
from asyncpg import UniqueViolationError

from exceptions.exceptions import ValidationError
from exceptions.schemas import FieldErrorModel

EXCEPTIONS_DIR = Path(__file__).parent


def handle_unique_violation_error(e: UniqueViolationError) -> None:
    error_msg = "Невозможно создать объект с указанными данными - такой объект уже существует"
    if hasattr(e, "constraint_name") and e.constraint_name:
        field = e.constraint_name[3:]
    else:
        field = re.search(r".*(uq_[a-z]+_[a-z]+).*", str(e))
        field = field.group()[3:] if field else ""

    raise ValidationError(
        field_errors=[FieldErrorModel(field=field, message=error_msg)],
    )


def load_error_translations() -> Dict[str, str]:
    translations_path = EXCEPTIONS_DIR.joinpath("translation/translations.json")

    with open(translations_path) as f:
        return json.load(f)


def get_error_type(exc: Exception) -> str:
    if isinstance(exc, ConnectionError):
        return "connection_error"
    elif isinstance(exc, TimeoutError):
        return "timeout_error"
    elif isinstance(exc, PostgresError):
        return "postgres_error"
    else:
        return "unknown_error"


def classify_exception_and_send_to_sentry(exc: Exception) -> None:
    error_type = get_error_type(exc)

    with sentry_sdk.push_scope() as scope:
        scope.set_tag("error_type", error_type)
        sentry_sdk.capture_exception(exc)
