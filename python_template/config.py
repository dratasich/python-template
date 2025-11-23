from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    # application debug mode
    debug: bool = False
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
