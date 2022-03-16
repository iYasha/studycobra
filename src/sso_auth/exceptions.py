from http import HTTPStatus

from fastapi import HTTPException
from starlette.authentication import AuthenticationError


class SSOBaseAuthException(AuthenticationError, HTTPException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = "unauthorized"

    def __init__(self, *args, **kwargs) -> None:
        status_code = kwargs.get("status_code") or self.status_code
        detail = kwargs.get("detail") or self.detail
        super().__init__(  # type: ignore
            status_code=status_code,
            detail=detail,
            *args,
            **kwargs,
        )


class SSOTokenNotFound(SSOBaseAuthException):
    detail = "token not found"


class SSOInvalidTokenFormat(SSOBaseAuthException):
    detail = "invalid token format"


class SSOInvalidToken(SSOBaseAuthException):
    detail = "invalid token"


class SSOExpiredTokenSignature(SSOBaseAuthException):
    detail = "expired token signature"


class SSOPermissionDenied(SSOBaseAuthException):
    detail = "no permission to perform this action"
    status_code = HTTPStatus.FORBIDDEN


class SSOUnathorized(SSOBaseAuthException):
    detail = "unathorized"
