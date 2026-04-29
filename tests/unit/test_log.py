from loguru import logger

from python_template.log import Level, configure


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
