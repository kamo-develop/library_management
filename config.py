from typing import Any

from environs import Env
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()
env.read_env(".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PG_SERVER: str = ""
    PG_PORT: int = 5432
    PG_USER: str = ""
    PG_PASSWORD: str
    PG_DATABASE: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
