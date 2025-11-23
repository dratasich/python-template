from python_template.infrastructure.repository import Repository


class DummyDatabaseClient:
    """Implements a dummy database client for testing purposes.

    In case the original one wants to connect on init.
    Otherwise consider using MagicMock or patching.
    """

    pass


def test_setup():
    repo = Repository(db_client=DummyDatabaseClient(), a_config_parameter="test")
    assert repo is not None
