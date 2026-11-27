from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Setting(BaseSettings):
    model_config = ConfigDict(env_file = BASE_PATH / ".env")
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_BOOKS: int = 60
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_PATH}/books.db"

    # @property
    # def db_url(self) -> str:
    #     return self.DATABASE_URL


setting = Setting()