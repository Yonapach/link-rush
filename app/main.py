from fastapi import FastAPI, Depends, Query
from pydantic import HttpUrl
from sqlalchemy import delete, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import get_first, get_session
from models import Url
from utils import get_uniq_short_path, is_short_path_exists

server = FastAPI()


@server.get("/create")
async def create_url(
    original_url: HttpUrl = Query(..., title="Original URL"), session: AsyncSession = Depends(get_session)
) -> str:
    original_url = original_url.unicode_string()
    stmt = select(Url).where(Url.original == original_url)

    url = await get_first(stmt, session)
    if not url:
        short_path = await get_uniq_short_path(session)
        url = Url(original=original_url, short=short_path)
        session.add(url)
        await session.commit()

    return url.absolute_short


@server.get("/delete")
async def delete_url(
    short_url: HttpUrl = Query(..., title="Short URL"), session: AsyncSession = Depends(get_session)
) -> int:
    """
    status
        0 - incorrect host
        1 - complete
        2 - not exists
    """
    #
    status = 0
    if short_url.host == settings.base_url.host:
        status = 2
        short_path = short_url.path.removeprefix("/")
        if await is_short_path_exists(short_path, session):
            stmt = delete(Url).where(Url.short == short_path)
            await session.execute(stmt)
            await session.commit()
            status = 1

    return status


@server.get("/get_original")
async def get_original_url(
    short_url: HttpUrl = Query(..., title="Short URL"), session: AsyncSession = Depends(get_session)
) -> str | None:
    if short_url.host == settings.base_url.host:
        short_path = short_url.path.removeprefix("/")
        stmt = select(Url.original).where(Url.short == short_path)
        original_url = await get_first(stmt, session)

        return original_url
