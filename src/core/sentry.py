import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration

from core.config import settings


def init_sentry(app):
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        release=settings.RELEASE,
        debug=settings.SENTRY_DEBUG,
        integrations=[LoggingIntegration(event_level=None)],
        request_bodies=settings.SENTRY_REQUEST_BODIES,
    )
    app.add_middleware(SentryAsgiMiddleware)

    return app
