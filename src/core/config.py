import os
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import HttpUrl
from pydantic import validator
from pydantic.networks import PostgresDsn


class Environment(Enum):
    PROD = "production"
    RC = "rc"
    STAGE = "stage"
    DEV = "dev"


class HardSettings:
    SWAGGER_URL: str = "/docs/"


class EnvSettings(BaseSettings):
    """
    Настройки из переменных окружения
    """

    # Main settings
    PROJECT_NAME: str = "Fastapi default"  # TODO: изменить название сервиса
    ENVIRONMENT: Optional[Environment] = None
    RELEASE: Optional[str] = None
    API_V1_STR: str = "/api/v1"
    URL_SUBPATH: str = ""
    DEBUG: Optional[bool] = True
    SENTRY_DSN: Optional[HttpUrl] = None
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    TESTING: bool = False

    # Database settings
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "app"
    DB_URI: Optional[PostgresDsn] = None

    @validator("DB_NAME", pre=True)
    def get_actual_db_name(cls, v: str, values: Dict[str, Any]) -> str:
        test_postfix = "_test"

        if values.get("TESTING") and not v.endswith(test_postfix):
            v += test_postfix
        return v

    @validator("DB_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Union[str, PostgresDsn]:
        if isinstance(v, str):
            return v

        path = values.get("DB_NAME", "")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{path}",
        )

    # RabbitMQ settings
    RABBIT_HOST: str = "localhost"
    RABBIT_PORT: int = 5672
    RABBIT_USERNAME: str = "guest"
    RABBIT_PASSWORD: str = "guest"
    RABBIT_VHOST: str = ""
    RABBIT_URL: Optional[str] = None

    @validator("RABBIT_URL", pre=True)
    def assemble_celery_broker_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return "amqp://{}:{}@{}:{}/{}".format(
            values.get("RABBIT_USERNAME"),
            values.get("RABBIT_PASSWORD"),
            values.get("RABBIT_HOST"),
            values.get("RABBIT_PORT"),
            values.get("RABBIT_VHOST"),
        )

    # Основные сервисы системы

    # SSO settings
    SSO_AUTH_JWT_KEY: str = ""
    SSO_AUTH_JWT_VERIFY_SIGNATURE: bool = False
    SSO_AUTH_JWT_ALGORITHMS: Union[List[str], str] = ["RS256"]

    @validator("SSO_AUTH_JWT_ALGORITHMS", pre=True)
    def validate_algoritms(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    SSO_AUTH_VALIDATION_ENABLED: bool = False
    SSO_VALIDATION_IGNORED_PATHS: List[str] = [
        "/api/v1/healthchecks/",
        f"{HardSettings.SWAGGER_URL}",
        "/docs",
        "/redoc",
    ]

    @validator("SSO_VALIDATION_IGNORED_PATHS", pre=True)
    def update_url_subpath(cls, v: List[str], values: Dict[str, Any]) -> List[str]:
        """
        Добавляет ко всем урлам, указанным в SSO_VALIDATION_IGNORED_PATHS,
        префикс URL_SUBPATH
        """
        url_subpath = values["URL_SUBPATH"]
        updated_path = []

        for path in v:
            updated_path.append(url_subpath + path)
        return updated_path


class SentrySettings(BaseSettings):
    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_DEBUG: bool = False
    SENTRY_REQUEST_BODIES: str = "always"


class Settings(HardSettings, EnvSettings, SentrySettings):
    @property
    def docs_url(self) -> str:
        return self.URL_SUBPATH + self.SWAGGER_URL

    @property
    def openapi_url(self) -> str:
        return self.URL_SUBPATH + self.SWAGGER_URL + "openapi.json"


settings = Settings()
