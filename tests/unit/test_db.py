from python_template.infrastructure.db import DatabaseClient


def test_db_url_password_not_logged(caplog):
    """Credentials embedded in the db_url must not appear in logs."""
    import logging

    with caplog.at_level(logging.INFO):
        DatabaseClient(db_url="postgresql://admin:s3cr3t@localhost/mydb")
    assert "s3cr3t" not in caplog.text
