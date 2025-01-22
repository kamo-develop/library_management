from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import NullPool

from config import settings

PG_URL = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_SERVER}:{settings.PG_PORT}/{settings.PG_DATABASE}"
TEST_PG_URL = f"postgresql+asyncpg://{settings.TEST_PG_USER}:{settings.TEST_PG_PASSWORD}@{settings.TEST_PG_SERVER}:{settings.TEST_PG_PORT}/{settings.TEST_PG_DATABASE}"

if settings.MODE == "TEST":
    DB_URL = TEST_PG_URL
    DB_PARAMS = {"poolclass": NullPool}
else:
    DB_URL = PG_URL
    DB_PARAMS = {}

engine = create_async_engine(DB_URL, **DB_PARAMS)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


