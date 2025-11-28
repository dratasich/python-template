import pytest
from _pytest.logging import LogCaptureFixture
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient
from loguru import logger

from python_template.api.middleware.log import LogMiddleware
from python_template.log import filter


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    """Replaces the standard caplog fixture to capture loguru logs."""
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def client():
    app = FastAPI()
    app.add_middleware(LogMiddleware)

    @app.get("/ping")
    def ping(request: Request):
        bound_logger = LogMiddleware.get_logger(request)
        bound_logger.debug("Ping endpoint called")
        return PlainTextResponse("pong")

    return TestClient(app)
