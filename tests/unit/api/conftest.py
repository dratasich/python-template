from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from python_template.api.demo import router as demo
from python_template.api.health import router as health
from python_template.config import Configuration
from python_template.infrastructure.repository import Repository


@pytest.fixture
def client():
    app = FastAPI()

    app.include_router(health.router)
    app.include_router(demo.router, prefix="/api/v1")

    # init router dependencies
    app.state.config = Configuration()
    db_client = MagicMock()
    db_client.is_connected.return_value = True
    app.state.db = db_client
    app.state.repo = Repository(
        db_client=db_client,
        a_config_parameter=["item1", "item2"],
    )

    return TestClient(app)
