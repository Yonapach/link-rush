import random
import string

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from models import Url

chars = string.ascii_uppercase + string.ascii_lowercase + string.digits


def get_random_str(length: int = 5) -> str:
    return "".join(random.choices(chars, k=length))


async def get_uniq_short_path(session: AsyncSession) -> str:
    while True:
        short_path = get_random_str()
        if not await is_short_path_exists(short_path, session):
            return short_path


async def is_short_path_exists(url: str, session: AsyncSession) -> bool:
    stmt = select(exists().where(Url.short == url))
    res = await session.execute(stmt)
    return res.scalar()
