from functools import wraps
from inspect import iscoroutinefunction
from typing import Any
from typing import Callable
from typing import List

from starlette.requests import Request

from sso_auth.config import SSOAuthConfig
from sso_auth.exceptions import SSOPermissionDenied
from sso_auth.exceptions import SSOUnathorized
from sso_auth.users import SSOUser
from sso_auth.utils import is_ignored_path


async def execute_view(func: Callable, request: Request, *args, **kwargs) -> Any:
    if iscoroutinefunction(func):
        return await func(request, *args, **kwargs)
    return func(request, *args, **kwargs)


# TODO удалить
def check_sso_groups(groups: List[str]) -> Callable:
    """Проверяет права на уровне групп пользователя."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):  # noqa: ANN201
            if not SSOAuthConfig.sso_auth_validation_enabled:
                return await execute_view(func, request, *args, **kwargs)

            if is_ignored_path(request.url.path):
                return await execute_view(func, request, *args, **kwargs)

            sso_user: SSOUser = request.user
            if not sso_user:
                raise SSOUnathorized

            is_access_granted = sso_user.has_common_groups(groups)
            if not is_access_granted:
                raise SSOPermissionDenied

            return await execute_view(func, request, *args, **kwargs)

        return wrapper

    return decorator


# TODO удалить
def check_sso_permissions(permissions: List[str]) -> Callable:
    """Проверяет права на уровне пермишенов юзера."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):  # noqa: ANN201
            if not SSOAuthConfig.sso_auth_validation_enabled:
                return await execute_view(func, request, *args, **kwargs)

            if is_ignored_path(request.url.path):
                return await execute_view(func, request, *args, **kwargs)

            sso_user: SSOUser = request.user
            if not sso_user:
                raise SSOUnathorized

            is_access_granted = sso_user.has_common_permissions(permissions)
            if not is_access_granted:
                raise SSOPermissionDenied

            return await execute_view(func, request, *args, **kwargs)

        return wrapper

    return decorator
