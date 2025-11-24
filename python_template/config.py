from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from python_template.log import Level


class Configuration(BaseSettings):
    # log level
    # see severity levels in https://loguru.readthedocs.io/en/stable/api/logger.html
    # uppercase value, see https://docs.pydantic.dev/1.10/usage/types/#constrained-types
    log_level: Level = Level.INFO
    # enable structured logging in JSON format
    log_json: bool = False

    # example secret value
    my_secret: SecretStr = SecretStr("set via env")
    # example list value from comma-separated string
    my_list_str: str | None = Field(alias="my_list", default=None)

    @property
    def my_list(self) -> list[str]:
        return self.my_list_str.split(",") if self.my_list_str else []

    model_config = SettingsConfigDict(
        extra="allow", env_file=(".env.shared", ".env.secret")
    )
