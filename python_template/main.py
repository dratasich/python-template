from loguru import logger

from python_template.config import Configuration
from python_template.infrastructure.db import DatabaseClient
from python_template.infrastructure.repository import Repository
from python_template.log import (
    configure as configure_logging,
)

# --- basic setup ---

config = Configuration()

configure_logging(level=config.log_level, enable_json=config.log_json)
logger.info(f"Configuration: {config}")

# --- init dependencies ---

repo = Repository(
    db_client=DatabaseClient(db_url="sqlite:///:memory:"),
    a_config_parameter=config.my_list,
)
response = repo.ping()
logger.info(f"Repo status: {response.value}")


def main():
    logger.info("Hello from python-template!")


if __name__ == "__main__":
    logger.info("Hello from python-template!")
