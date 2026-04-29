"""Database client.

May be shared across the application.
Should limit the number of connections to the database
(your ops-colleagues will be thankful ;).
"""

import random
from urllib.parse import urlparse, urlunparse

from loguru import logger


def _sanitize_url(url: str) -> str:
    """Strip credentials from a database URL before logging."""
    try:
        parsed = urlparse(url)
        sanitized = parsed._replace(netloc=parsed.hostname or "")
        return urlunparse(sanitized)
    except Exception:
        return "<unparseable url>"


class DatabaseClient:
    def __init__(self, db_url: str):
        logger.info(f"Connecting to database at {_sanitize_url(db_url)}")

    def is_connected(self) -> bool:
        logger.trace("Checking database connection")
        return random.choice([True, False])  # noqa: S311 - mock stub, not crypto
