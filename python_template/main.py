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

db_client = DatabaseClient(db_url="sqlite:///:memory:")
repo = Repository(
    db_client=db_client,
    a_config_parameter=config.my_list,
)
try:
    response = repo.get(item_id=1)
    logger.info(f"Get item: {response}")
except Exception as e:
    logger.error(f"Error getting item: {e}")

if __name__ == "__main__":
    logger.info("Hello from python-template!")
