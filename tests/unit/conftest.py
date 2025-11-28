from unittest.mock import MagicMock

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from python_template.infrastructure.repository import Repository
from python_template.log import filter


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    """Replaces the standard caplog fixture to capture loguru logs.

    https://loguru.readthedocs.io/en/stable/resources/migration.html#replacing-caplog-fixture-from-pytest-library
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level
        and filter(record),
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def db_mock():
    db_client = MagicMock()
    db_client.is_connected.return_value = True
    return db_client


@pytest.fixture
def repo(db_mock):
    return Repository(db_client=db_mock)
