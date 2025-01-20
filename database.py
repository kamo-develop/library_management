from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from config import settings

PG_URL = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_SERVER}:{settings.PG_PORT}/{settings.PG_DATABASE}"

engine = create_async_engine(PG_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


