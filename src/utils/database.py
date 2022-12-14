from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from utils.settings import settings


Base = declarative_base()

engine = create_async_engine(
    f'postgresql+asyncpg://{settings.DB_USERNAME}:'
    f'{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSession(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    try:
        yield session
    finally:
        await session.close()
