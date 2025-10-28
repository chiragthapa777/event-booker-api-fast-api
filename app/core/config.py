from typing import Optional
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.enums.env_enum import Env


class AppConfig(BaseSettings):
    env: Env
    app_name: str
    port: int = 8080
    debug: bool = True
    host: str = "localhost"
    db_url: str | None
    access_token_secret: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_bucket_name: str

    model_config = SettingsConfigDict(env_file=".env")

    @computed_field
    @property
    def echo_query(self) -> bool:
        return self.env == Env.LOCAL


_settings: Optional[AppConfig] = None


def setup_config():
    global _settings
    _settings = AppConfig()


def get_config():
    return _settings
