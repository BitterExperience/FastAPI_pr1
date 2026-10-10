from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI


from app.db.session import engine


from app.routers import book_router, author_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()



app = FastAPI(lifespan=lifespan)

app.include_router(book_router)
app.include_router(author_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)