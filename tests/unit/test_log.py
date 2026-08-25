import logging

import pytest
from loguru import logger

from python_template.log import Level, configure, stdlib_level


def test_plain_text_logger_diagnose_off(capsys):
    """Local variable values must not appear in plain-text tracebacks.

    diagnose=True would annotate call sites with the argument values
    (e.g. inner(secret) → └ 'super_secret_value').
    diagnose=False must suppress that annotation.
    """
    configure(level=Level.ERROR, enable_json=False)

    def inner(arg):
        raise RuntimeError("generic error")

    def outer():
        local_secret = "super_secret_value"  # noqa: S105  # pragma: allowlist secret
        inner(local_secret)  # diagnose=True would annotate the argument value here

    try:
        outer()
    except RuntimeError:
        logger.exception("caught")

    captured = capsys.readouterr()
    assert "super_secret_value" not in captured.err


@pytest.mark.parametrize(
    ("app_level", "expected"),
    [
        (Level.DEBUG, "DEBUG"),
        (Level.INFO, "INFO"),
        (Level.WARNING, "WARNING"),
        (Level.ERROR, "ERROR"),
        (Level.CRITICAL, "CRITICAL"),
        # stdlib logging has no TRACE/SUCCESS, map to closest level
        (Level.TRACE, "DEBUG"),
        (Level.SUCCESS, "INFO"),
    ],
)
def test_stdlib_level_mapping(app_level, expected):
    assert stdlib_level(app_level) == expected


@pytest.mark.parametrize(
    ("app_level", "expected"),
    [
        (Level.DEBUG, logging.DEBUG),
        (Level.INFO, logging.INFO),
        (Level.WARNING, logging.WARNING),
    ],
)
def test_stdlib_root_level_follows_app_level(app_level, expected):
    """The stdlib root logger must not stay at level 0.

    With root at level 0, every stdlib record (e.g. kafka-python's
    internal TRACE/DEBUG logs) is formatted and bridged to loguru,
    and dropped only at the sink.
    """
    root = logging.getLogger()
    original = root.level
    try:
        configure(level=app_level)
        assert root.level == expected
    finally:
        root.setLevel(original)


def test_third_party_debug_is_filtered_at_source():
    """Noisy third-party loggers (kafka-python) must not emit DEBUG."""
    root = logging.getLogger()
    original = root.level
    try:
        configure(level=Level.INFO)
        assert not logging.getLogger("kafka.producer.kafka").isEnabledFor(logging.DEBUG)
    finally:
        root.setLevel(original)


def test_configure_is_recallable():
    """configure() must not crash when called twice (e.g. app + tests)."""
    root = logging.getLogger()
    original = root.level
    try:
        configure(level=Level.INFO)
        configure(level=Level.INFO)
    finally:
        root.setLevel(original)
