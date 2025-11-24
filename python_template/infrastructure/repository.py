from loguru import logger

from .db import DatabaseClient
from .repository_status import RepositoryStatus


class Repository:
    def __init__(self, db_client: DatabaseClient, a_config_parameter: list[str]):
        self.__db = db_client
        logger.info(f"Initializing repository with parameter: {a_config_parameter}")

    def ping(self) -> RepositoryStatus:
        logger.debug("Ping called on repository")
        if self.__db.is_connected():
            logger.debug("Database is connected")
            return RepositoryStatus.CONNECTED
        logger.warning("Database is not connected")
        return RepositoryStatus.UNKNOWN
