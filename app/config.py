from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    base_url: HttpUrl


settings = Settings()
