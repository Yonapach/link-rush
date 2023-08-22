from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, DeclarativeBase

from config import settings
from utils import get_short_path


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return "".join(["_" + i.lower() if i.isupper() else i for i in cls.__name__]).lstrip("_")


class Url(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    original: Mapped[str] = mapped_column(unique=True, index=True)

    @property
    def short(self) -> str:
        return settings.base_url.unicode_string() + get_short_path(self.id)
