from pathlib import Path
from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).resolve().parent.parent.parent


class Setting(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def db_url(self) -> str:
        return f"sqlite+aiosqlite:///{BASE_PATH}/books.db"


    class Config:
        env_file = BASE_PATH / ".env"

setting = Setting()