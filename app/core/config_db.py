from pydantic_settings import BaseSettings




class Setting(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///./books.db"


setting = Setting()