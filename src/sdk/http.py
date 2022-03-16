import logging
from typing import Dict

from sso_auth.config import SSOAuthConfig
from starlette.requests import Request

REGISTRY_SERVICE_LOGGER = logging.getLogger("registry_client")
SRM_SERVICE_LOGGER = logging.getLogger("srm_client")
MDM_SERVICE_LOGGER = logging.getLogger("mdm_client")


AUTHORIZATION_HEADER_NAME = SSOAuthConfig.authorization_header_name


def _get_headers(request: Request) -> Dict[str, str]:
    headers = {}
    token = request.headers.get(SSOAuthConfig.authorization_header_name)
    headers[AUTHORIZATION_HEADER_NAME] = token

    return headers
