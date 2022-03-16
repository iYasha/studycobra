from logging import config as logging_config

import uvicorn
from api.routes import api_router
from core.config import Settings
from core.config import settings
from core.database import database
from core.logging_conf import LOGGING
from core.sentry import init_sentry
from fastapi.params import Security
from exceptions.exception_handler_mapping import exception_handler_mapping
from logger.in_requests.application import DefaultFastAPI
from sso_auth.authentication import SSOAuthBackend
from sso_auth.config import SSOAuthConfig
from sdk.exceptions import auth_exception_handler
from sdk.security import fake_http_bearer
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

logging_config.dictConfig(LOGGING)

app = DefaultFastAPI(
    service_code="",  # TODO: задать код сервиса
    title=settings.PROJECT_NAME,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    exception_handlers=exception_handler_mapping,
    dependencies=[
        Security(fake_http_bearer),
    ],
)

# Routers
app.include_router(api_router, prefix=settings.URL_SUBPATH + settings.API_V1_STR)

# Middlewares
app.add_middleware(
    AuthenticationMiddleware,
    backend=SSOAuthBackend(),
    on_error=auth_exception_handler,
)

if settings.SENTRY_DSN:
    app = init_sentry(app)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@SSOAuthConfig.load_config
def get_config() -> Settings:
    return settings


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8006, access_log=False, reload=True)
