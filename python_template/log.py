import sys

from loguru import logger


def configure_logging(level="INFO", enable_json=True):
    """Configures root logger.

    Levels are identified by their names.
    """
    logger.remove(0)  # remove the default handler configuration

    # POSIX standard -> diagnostic output to stderr
    if enable_json:
        # simplify loguru's default JSON format
        # requires tweaking
        logger.add(sys.stderr, format="{message}", level=level, serialize=enable_json)
    else:
        # default loguru format with colorization
        logger.add(sys.stderr, level=level)
