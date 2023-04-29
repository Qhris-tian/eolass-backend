import logging
from functools import lru_cache

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str = "Eolass Backend"
    API_VERSION: str = "v1"
    ALLOWED_ORIGINS: str = "*"
    ENVIRONMENT: str = "development"
    APP_HASH_ALGRORITHM: str = "HS256"
    DATABASE_NAME: str = "eolass_db"
    LOG_LEVEL = logging.WARNING
    ENEBA_BASE_URI: str = ""
    ENEBA_CLIENT_ID: str = ""
    ENEBA_GRANT_TYPE: str = ""
    ENEBA_ID: str = ""
    ENEBA_SECRET: str = ""
    EZPIN_BASE_URI: str = ""
    EZPIN_VERSION: str = "v2"
    EZPIN_ID: str = ""
    EZPIN_SECRET: str = ""

    class Config:
        env_file = ".env"

    @validator("EZPIN_BASE_URI")
    @classmethod
    def get_ezpin_base_uri(cls, value: str, values) -> str:
        return "{}/{}".format(value, values["EZPIN_VERSION"])


@lru_cache()
def get_settings() -> Settings:
    return Settings()
