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
    PROJECT_NAME: str = "Fastapi default"
    ENVIRONMENT: Optional[Environment] = None
    FULL_DOMAIN: Optional[str] = None
    RELEASE: Optional[str] = None
    API_V1_STR: str = "/api/v1"
    URL_SUBPATH: str = ""
    DEBUG: Optional[bool] = True
    SENTRY_DSN: Optional[HttpUrl] = None
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    TESTING: bool = False
    SECRET_KEY: str = ''

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app"
    DB_URI: Optional[PostgresDsn] = None

    @validator("POSTGRES_DB", pre=True)
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

        path = values.get("POSTGRES_DB", "")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{path}",
        )

    # RabbitMQ settings
    RABBIT_HOST: str = "localhost"
    RABBIT_PORT: int = 5672
    RABBIT_USERNAME: str = "guest"
    RABBIT_PASSWORD: str = "guest"
    RABBIT_VHOST: str = ""
    RABBIT_URL: Optional[str] = None

    # Celery settings
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_TIMEZONE = "Europe/Kiev"
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_TASK_SERIALIZER = "json"
    CELERYD_MAX_TASKS_PER_CHILD: int = 1


    @validator("RABBIT_URL", 'CELERY_BROKER_URL', pre=True)
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
    SSO_AUTH_JWT_KEY: str = "test"
    SSO_AUTH_JWT_VERIFY_SIGNATURE: bool = False
    SSO_AUTH_JWT_ALGORITHMS: Union[List[str], str] = ["HS256"]
    SSO_ACCESS_TOKEN_EXPIRE_MINUTES: int = 48 * 60
    SSO_REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60

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
