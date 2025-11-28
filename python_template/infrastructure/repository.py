"""Wrapper around the database.

In case you have to change the database
this pattern helps to isolate the changes - a life saver ;)

See also:
- https://www.umlboard.com/design-patterns/repository.html
- https://fastapi.tiangolo.com/tutorial/sql-databases/
"""

from loguru import logger

from .db import DatabaseClient


class Repository:
    def __init__(
        self,
        db_client: DatabaseClient,
        a_config_parameter: list[str] | None = None,
    ):
        self.__db = db_client
        self.__cache: dict[int, str] = {}
        if a_config_parameter is not None:
            self.__cache = {
                id: value for id, value in enumerate(a_config_parameter, start=1)
            }
        logger.info(f"Initialized repository with {len(self.__cache)} items")

    def _check_ready(self):
        """Check if the repository is ready to serve requests.

        Raises:
            ConnectionError: If the database is not connected.
        """
        if not self.__db.is_connected():
            logger.warning("Database is not connected")
            raise ConnectionError("Database is not connected")

    def put(self, item: str) -> int:
        self._check_ready()
        item_id = len(self.__cache) + 1
        self.__cache[item_id] = item
        logger.debug(f"Storing item with id: {item_id}")
        return item_id

    def get(self, item_id: int) -> str | None:
        self._check_ready()
        logger.debug(f"Getting item with id: {item_id}")
        return self.__cache.get(item_id, None)
