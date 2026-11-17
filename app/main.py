from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.core.cors import origins

from app.routers import book_router, author_router, user_router, admin_router
from app.middleware.logging import log_requests


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
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
