from contextlib import asynccontextmanager
from typing import AsyncGenerator

from pymongo import AsyncMongoClient

from app.setup.config.settings import MongodbUri


@asynccontextmanager
async def get_mongo_client(
    mongodb_url: MongodbUri
) -> AsyncGenerator[AsyncMongoClient, None]:
    async with AsyncMongoClient(mongodb_url) as client:
        yield client
