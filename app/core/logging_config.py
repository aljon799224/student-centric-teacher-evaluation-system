"""Logging Config."""

import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "uvicorn": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "app": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
}


def setup_logging():
    """Setup logging."""
    logging.config.dictConfig(LOGGING_CONFIG)
