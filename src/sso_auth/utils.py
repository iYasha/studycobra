from typing import Optional

import jwt
from jwt import DecodeError
from jwt import ExpiredSignatureError
from jwt import InvalidAlgorithmError
from jwt import InvalidSignatureError
from starlette.authentication import UnauthenticatedUser
from starlette.requests import Request

from sso_auth.config import SSOAuthConfig
from sso_auth.exceptions import SSOExpiredTokenSignature
from sso_auth.exceptions import SSOInvalidToken
from sso_auth.middlewares import ctx_var
from sso_auth.users import SSOUser


def is_ignored_path(path: str) -> bool:
    for ignored_path in SSOAuthConfig.sso_validation_ignored_paths:  # noqa: SIM110
        if path.startswith(ignored_path):
            return True
    return False


def get_user_data_from_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            key=SSOAuthConfig.sso_auth_jwt_key,
            verify=SSOAuthConfig.sso_auth_jwt_verify_signature,
            algorithms=SSOAuthConfig.sso_auth_jwt_algorithms,
        )
    except (DecodeError, InvalidSignatureError, InvalidAlgorithmError):
        raise SSOInvalidToken
    except ExpiredSignatureError:
        raise SSOExpiredTokenSignature


def get_sso_user_info() -> Optional[SSOUser]:
    """ Получить данные пользователя из request."""

    request: Request = ctx_var.get()
    if not request:
        return None

    user: SSOUser = request.scope["user"]
    if isinstance(user, UnauthenticatedUser):
        return None

    return user
