from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Setting(BaseSettings):
    model_config = ConfigDict(env_file = BASE_PATH / ".env")
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def db_url(self) -> str:
        return f"sqlite+aiosqlite:///{BASE_PATH}/books.db"


setting = Setting()