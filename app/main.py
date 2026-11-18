from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from app.db.session import engine
from app.core.cors import origins
from app.routers import book_router, author_router, user_router, admin_router
from app.middleware.logging import log_requests
from app.core.config_db import setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.radis = Redis.from_url(setting.REDIS_URL, decode_responses=True)
    yield
    await app.state.redis.aclose()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(book_router)
app.include_router(author_router)
app.include_router(user_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
