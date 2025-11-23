from python_template.config import Configuration


# https://docs.pytest.org/en/stable/how-to/monkeypatch.html
def test_env_override(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    config = Configuration()
    assert config.debug is True


def test_secret_not_printed():
    config = Configuration(my_secret="password")
    config_str = str(config)
    assert "password" not in config_str


def test_my_list_property():
    config = Configuration(my_list="x,y,z")
    assert config.my_list == ["x", "y", "z"]


def test_extra_fields_allowed():
    config = Configuration(extra_field="extra")
    assert hasattr(config, "extra_field")
    assert config.extra_field == "extra"
