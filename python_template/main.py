import uvicorn
from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from python_template.api.demo import router as demo
from python_template.api.health import router as health
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

# --- fastapi app ---

app = FastAPI(
    summary="Python Template Service",
    description="A template for Python microservices using FastAPI.",
    version="0.1.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# add routers
# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# add health endpoints / k8s probes
app.include_router(health.router, include_in_schema=False)
app.include_router(demo.router, prefix="/api/v1", tags=["demo"])

# add dependencies to app state so they can be accessed in endpoints
app.state.config = config
app.state.db = db_client
app.state.repo = repo

# expose fastapi metrics in prometheus format
Instrumentator().instrument(app).expose(app, include_in_schema=False)


if __name__ == "__main__":
    logger.info("Run webserver...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,  # disable uvicorn to overwrite our log config
        log_level=None,
    )  # blocking
    logger.info("Application stopped.")
