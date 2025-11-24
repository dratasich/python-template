"""Logging configuration.

We use [loguru](https://loguru.readthedocs.io/en/stable/)
and have the setup from the following guide(s):
- [Production-Grade Python Logging Made Easier with Loguru](https://www.dash0.com/guides/python-logging-with-loguru)
"""

import json
import logging
import sys
import traceback
from enum import StrEnum

from loguru import logger


class Level(StrEnum):
    """Log levels.

    We may add more levels, so we define the ones available for the app here.
    See severity levels in [loguru documentation](https://loguru.readthedocs.io/en/stable/api/logger.html).
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def configure(level=Level.INFO, enable_json=False):
    """Configures loguru.

    Wraps the logging setup into a function
    to avoid implicit configuration on import,
    or a longer setup function in main.py.
    Unfortunately, I couldn't find a way to have type checking
    (`from loguru import Logger`).
    """
    logger.remove(0)  # remove the default handler configuration

    # POSIX standard -> diagnostic output to stderr
    # levels are simple uppercase strings

    if enable_json:
        # simplify loguru's default JSON format with a custom serializer
        logger.add(
            sys.stderr,
            format="{serialized}",
            level=level.value,
            diagnose=False,  # avoid leaking sensitive data
        )
        logger.configure(patcher=patching)
    else:
        # default loguru format with colorization
        logger.add(sys.stderr, level=level.value)

    # intercept all logs from the standard logging module
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def serialize(record):
    """Returns a custom JSON serialization of a loguru record."""
    subset = {
        "timestamp": record["time"].isoformat(),
        "log": {
            "level": record["level"].name,
            "name": record["name"],
            "function": record["function"],
            "line": record["line"],
        },
        "message": record["message"],
    }

    # Merge extra fields directly into the top-level dict
    if record["extra"]:
        subset.update(record["extra"])

    if record["exception"]:
        exc = record["exception"]
        subset["exception"] = {
            "type": exc.type.__name__,
            "value": str(exc.value),
            "traceback": traceback.format_exception(exc.type, exc.value, exc.traceback),
        }

    return json.dumps(subset)


def patching(record):
    """Add our custom serialization to the loguru record."""
    record["serialized"] = serialize(record)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        global logger

        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
