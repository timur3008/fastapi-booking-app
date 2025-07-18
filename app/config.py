from typing import Literal

from pydantic import BaseSettings, root_validator


class MyConfig(BaseSettings.Config):
    env_file = ".env"


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]  # проверяет входит ли значение в одну из них
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @root_validator
    def get_database_url(cls, v):
        v["DATABASE_URL"] = (
            f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        )
        return v

    @root_validator
    def get_test_database_url(cls, v):
        v["TEST_DATABASE_URL"] = (
            f"postgresql+asyncpg://{v['TEST_DB_USER']}:{v['TEST_DB_PASS']}@{v['TEST_DB_HOST']}:{v['TEST_DB_PORT']}/{v['TEST_DB_NAME']}"
        )
        return v

    Config = MyConfig


settings = Settings()