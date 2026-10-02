from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)
from typing import AsyncGenerator

from app.core.config_db import setting


engine = create_async_engine(setting.DB_URL, echo=True)

session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with setting.session() as conn:
        yield conn
