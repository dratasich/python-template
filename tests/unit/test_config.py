from python_template.config import Configuration


# https://docs.pytest.org/en/stable/how-to/monkeypatch.html
def test_env_override(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "TRACE")
    config = Configuration()
    assert config.log_level == "TRACE"


def test_secret_not_printed(monkeypatch):
    monkeypatch.setenv("MY_SECRET", "password")
    config = Configuration()
    config_str = str(config)
    assert "password" not in config_str


def test_my_list_property(monkeypatch):
    monkeypatch.setenv("MY_LIST", "x,y,z")
    config = Configuration()
    assert config.my_list == ["x", "y", "z"]


def test_extra_fields_allowed(monkeypatch):
    monkeypatch.setenv("EXTRA_ENV", "extra")
    config = Configuration()
    assert not hasattr(config, "extra_field")
