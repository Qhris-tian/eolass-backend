import logging
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Eolass Backend"
    api_version: str = "v1"
    allowed_origins: str = "*"
    environment: str = "development"
    app_hash_algorithm: str = "HS256"
    database_name: str = "eolass_db"
    test_database_name: str = "test"
    log_level = logging.WARNING

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()