from loguru import logger


def test_logging(caplog):
    logger.info("Hello from python-template!")
    assert "Hello from python-template!" in caplog.text
