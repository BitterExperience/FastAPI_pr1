from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Setting(BaseSettings):
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/books.db"


setting = Setting()