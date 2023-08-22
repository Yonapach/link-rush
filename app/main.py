from fastapi import FastAPI, Depends, Body
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db import get_first, get_session
from models import Url
from utils import get_id

server = FastAPI()


@server.post("/create")
async def create_url(
    original_url: HttpUrl = Body(..., title="Original URL"), session: AsyncSession = Depends(get_session)
) -> str:
    original_url = original_url.unicode_string()
    stmt = select(Url).where(Url.original == original_url)
    url_obj = await get_first(stmt, session)

    if not url_obj:
        url_obj = Url(original=original_url)
        session.add(url_obj)
        await session.commit()

    return url_obj.short


@server.post("/delete")
async def delete_url(
    short_url: HttpUrl = Body(..., title="Short URL"), session: AsyncSession = Depends(get_session)
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

        if url_id := get_id(short_path):
            if url_obj := await session.get(Url, url_id):
                await session.delete(url_obj)
                await session.commit()
                status = 1

    return status


@server.post("/get_original")
async def get_original_url(
    short_url: HttpUrl = Body(..., title="Short URL"), session: AsyncSession = Depends(get_session)
) -> str | None:
    if short_url.host == settings.base_url.host:
        short_path = short_url.path.removeprefix("/")

        if url_id := get_id(short_path):
            if url_obj := await session.get(Url, url_id):
                return url_obj.original
