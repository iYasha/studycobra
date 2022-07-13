from fastapi.exceptions import RequestValidationError

from exceptions.exceptions import ValidationError
# from exceptions.handlers import auth_exception_handler
from exceptions.handlers import logic_validation_exception_handler
from exceptions.handlers import not_found_exception_handler
from exceptions.handlers import request_validation_exception_handler
from exceptions.handlers import unexpected_exception_handler
# from sso_auth.exceptions import SSOBaseAuthException

exception_handler_mapping = {
    Exception: unexpected_exception_handler,
    # SSOBaseAuthException: auth_exception_handler,
    404: not_found_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    ValidationError: logic_validation_exception_handler,
}
