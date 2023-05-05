from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import Settings, get_settings


def get_database_client(database_dsn) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(database_dsn)


def get_database(settings: Settings = Depends(get_settings)):
    client = get_database_client(settings.DATABASE_DSN)
    return client[settings.DATABASE_NAME]


async def drop_test_database():  # pragma: no cover
    settings = get_settings()
    client = get_database_client(settings.DATABASE_DSN)
    await client.drop_database("test")
