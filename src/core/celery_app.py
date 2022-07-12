import asyncio
from logging import config as logging_config

import sentry_sdk
from celery import Celery
from celery.signals import worker_process_init
from celery.signals import worker_process_shutdown
from core.config import settings
from core.logging_conf import LOGGING
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


logging_config.dictConfig(LOGGING)


# @worker_process_init.connect
# def set_sentry(*args, **kwargs) -> None:
#     loop = asyncio.get_event_loop()
#     if not database.is_connected:
#         loop.run_until_complete(database.connect())
#     if settings.SENTRY_DSN:
#         if settings.SENTRY_DSN:
#             sentry_sdk.init(
#                 dsn=settings.SENTRY_DSN,
#                 environment=settings.ENVIRONMENT,
#                 release=settings.RELEASE,
#                 debug=settings.SENTRY_DEBUG,
#                 integrations=[LoggingIntegration(event_level=None), SqlalchemyIntegration(), CeleryIntegration()],
#                 request_bodies=settings.SENTRY_REQUEST_BODIES,
#             )
#
#
# @worker_process_shutdown.connect
# def shutdown(*args, **kwargs) -> None:
#     loop = asyncio.get_event_loop()
#     if database.is_connected:
#         loop.run_until_complete(database.disconnect())


celery_app = Celery('studycobra')
celery_app.config_from_object(settings, namespace="CELERY")

