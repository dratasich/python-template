import random

from loguru import logger


class DatabaseClient:
    def __init__(self, db_url: str):
        logger.info(f"Connecting to database at {db_url}")

    def is_connected(self) -> bool:
        logger.debug("Checking database connection")
        return random.choice([True, False])
