import sys
import logging
from logging import handlers
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

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def setup_root_logger():
    """ Setup configuration of the root logger of the application """

    # get instance of root logger
    logger = logging.getLogger('')

    # configure formatter for logger
    formatter = logging.Formatter(LOG_FORMAT)

    # configure console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # configure rotating file handler
    file = handlers.RotatingFileHandler(
        filename="logs/elk-logs.log", mode='a',
        maxBytes=15000000, backupCount=5
    )
    file.setFormatter(formatter)

    # add handlers
    logger.addHandler(console)
    logger.addHandler(file)

    # configure logger level
    logger.setLevel(logging.INFO)
