from typing import Callable
from typing import List

from pydantic import BaseModel


class SSOConfigModel(BaseModel):
    sso_auth_jwt_key: str = ""
    sso_auth_jwt_verify_signature: bool = False
    sso_auth_jwt_algorithms: List[str] = ["RS256"]
    sso_auth_validation_enabled: bool = False
    sso_validation_ignored_paths: List[str] = []
    bearer_prefix: str = "Bearer "
    authorization_header_name: str = "Authorization"


class SSOAuthConfig:
    bearer_prefix: str = "Bearer "
    authorization_header_name: str = "Authorization"

    sso_auth_jwt_key: str = ""
    sso_auth_jwt_verify_signature: bool = False
    sso_auth_jwt_algorithms: List[str] = ["RS256"]
    sso_auth_validation_enabled: bool = False
    sso_validation_ignored_paths: List[str] = []

    @classmethod
    def load_config(cls, settings: Callable[..., List[tuple]]) -> "SSOAuthConfig":  # type: ignore
        config = SSOConfigModel(**{key.lower(): value for key, value in settings()})

        cls.bearer_prefix = config.bearer_prefix
        cls.authorization_header_name = config.authorization_header_name

        cls.sso_auth_jwt_key = config.sso_auth_jwt_key
        cls.sso_auth_jwt_verify_signature = config.sso_auth_jwt_verify_signature
        cls.sso_auth_jwt_algorithms = config.sso_auth_jwt_algorithms
        cls.sso_auth_validation_enabled = config.sso_auth_validation_enabled
        cls.sso_validation_ignored_paths = config.sso_validation_ignored_paths
