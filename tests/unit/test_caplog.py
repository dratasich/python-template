from loguru import logger


def test_logging(caplog):
    logger.info("Hello from python-template!")
    assert "Hello from python-template!" in caplog.text


def test_filtering(caplog):
    logger.info("GET /live endpoint called")
    logger.info("This is a regular log message")
    assert "This is a regular log message" in caplog.text
    assert "GET /live endpoint called" not in caplog.text
