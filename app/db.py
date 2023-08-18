from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from config import settings

async_engine = create_async_engine(settings.db_url)
# async_engine = create_async_engine(settings.db_url, echo=True)
async_session = async_sessionmaker(async_engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


async def get_first(stmt: select, session: AsyncSession):
    res = await session.execute(stmt.limit(1))
    return res.scalar()
