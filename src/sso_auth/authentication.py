from typing import Optional

from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.requests import Request

from sso_auth.config import SSOAuthConfig
from sso_auth.exceptions import SSOBaseAuthException
from sso_auth.exceptions import SSOInvalidTokenFormat
from sso_auth.exceptions import SSOTokenNotFound
from sso_auth.users import make_sso_user
from sso_auth.utils import get_user_data_from_token
from sso_auth.utils import is_ignored_path


class SSOAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request) -> Optional[tuple]:

        if not SSOAuthConfig.sso_auth_validation_enabled:
            return None

        if is_ignored_path(request.url.path):
            return None

        try:
            token: Optional[str] = request.headers.get(SSOAuthConfig.authorization_header_name)
            if not token:
                raise SSOTokenNotFound

            if not token.startswith(SSOAuthConfig.bearer_prefix):
                raise SSOInvalidTokenFormat
            token = token[len(SSOAuthConfig.bearer_prefix) :]

            user_data = get_user_data_from_token(token)
            sso_user = make_sso_user(user_data)
        except SSOBaseAuthException as sso_base_auth_exception:
            raise sso_base_auth_exception

        return AuthCredentials(), sso_user
