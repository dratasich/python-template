"""Database client.

May be shared across the application.
Should limit the number of connections to the database
(your ops-colleagues will be thankful ;).
"""

import random

from loguru import logger


class DatabaseClient:
    def __init__(self, db_url: str):
        logger.info(f"Connecting to database at {db_url}")

    def is_connected(self) -> bool:
        logger.trace("Checking database connection")
        return random.choice([True, False])
