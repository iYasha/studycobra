import logging

import structlog
from structlog.contextvars import merge_contextvars
from structlog_sentry import SentryProcessor

from .processors import add_service_code


class DefaultLoggerFactory(structlog.stdlib.LoggerFactory):
    """Фабрика structlog-логеров, прокидывающая код сервиса в логгер."""

    def __init__(self, service_code: str = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.service_code = service_code

    def __call__(self, *args) -> logging.Logger:
        logger_ = super().__call__(*args)
        logger_.service_code = self.service_code  # type: ignore
        return logger_


def configure_structlog_logger(service_code: str) -> None:
    if structlog.is_configured():
        return

    structlog.configure(
        processors=[
            merge_contextvars,
            add_service_code,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            SentryProcessor(level=logging.ERROR),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=DefaultLoggerFactory(service_code),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
