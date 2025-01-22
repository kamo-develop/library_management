from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    MODE: Literal["DEV", "TEST", "PROD"]

    PG_SERVER: str = ""
    PG_PORT: int = 5432
    PG_USER: str = ""
    PG_PASSWORD: str
    PG_DATABASE: str

    TEST_PG_SERVER: str = ""
    TEST_PG_PORT: int = 5432
    TEST_PG_USER: str = ""
    TEST_PG_PASSWORD: str
    TEST_PG_DATABASE: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str


settings = Settings()
