from typing import List

from starlette.requests import Request

from sso_auth.config import SSOAuthConfig
from sso_auth.exceptions import SSOPermissionDenied
from sso_auth.exceptions import SSOUnathorized
from sso_auth.users import SSOUser
from sso_auth.utils import is_ignored_path


class PermissionsChecker:
    def __init__(self, permissions: List[str]) -> None:
        self.permissions = permissions

    def __call__(self, request: Request) -> None:
        if not SSOAuthConfig.sso_auth_validation_enabled:
            return

        if is_ignored_path(request.url.path):
            return

        sso_user: SSOUser = request.user
        if not sso_user:
            raise SSOUnathorized

        is_access_granted = sso_user.has_common_permissions(self.permissions)
        if not is_access_granted:
            raise SSOPermissionDenied
