import sys

import structlog

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "logging": {"handlers": ["console"], "level": "INFO"},
        # TODO: добавьте необходимые логгеры
    },
}
