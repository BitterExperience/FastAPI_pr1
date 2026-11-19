from typing import Annotated, Any

from alembic.util import status
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.crud import create_book, get_one_book, get_all_books, update_book, delete_book
from app.db.session import get_db
from app.schemas import CreateBook, BookResponse
from app.security.dependencies import get_current_active_user
from app.models.user import UserModel
from app.core.redis import get_redis
from app.core.config_db import setting
from app.services.cache import get_or_set, invalidate_all_books, invalidate_book

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", status_code=201)
async def create_book_endpoint(data: CreateBook, db: Annotated[AsyncSession, Depends(get_db)],
                               current_user: Annotated[UserModel, Depends(get_current_active_user)],
                               redis: Annotated[Redis, Depends(get_redis)]
                               ) -> BookResponse:
    data_book = data.model_dump()
    data_book["created_by"] = current_user.id
    book = await create_book(data_book, db)
    await invalidate_all_books(redis)
    return book


async def _load_books(db):
    books = await get_all_books(db)
    return [BookResponse.model_validate(b).model_dump() for b in books]


@router.get("")
async def get_all_endpoint(db: Annotated[AsyncSession, Depends(get_db)],
                           redis: Annotated[Redis, Depends(get_redis)]
                           ) -> list[BookResponse]:
    return await get_or_set(redis, "books:all", setting.CACHE_TTL_BOOKS, lambda: _load_books(db))


async def _load_one_book(book_id, db) -> dict[str, Any] | None:
    book = await get_one_book(book_id, db)
    if book is None:
        return None
    return BookResponse.model_validate(book).model_dump()


@router.get("/{book_id}")
async def get_one_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                                db: Annotated[AsyncSession, Depends(get_db)],
                                redis: Annotated[Redis, Depends(get_redis)]
                                ) -> BookResponse:
    cache = await get_or_set(redis, f"book:{book_id}",
                             setting.CACHE_TTL_BOOKS,
                             lambda: _load_one_book(book_id, db))
    if cache is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return cache


@router.put("/{book_id}", status_code=200)
async def update_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                               data: CreateBook,
                               db: Annotated[AsyncSession, Depends(get_db)],
                               current_user: Annotated[UserModel, Depends(get_current_active_user)],
                               redis: Annotated[Redis, Depends(get_redis)]
                               ) -> BookResponse:
    book_found = await get_one_book(book_id, db)

    if book_found is None:
        raise HTTPException(404, f"Book {book_id} not found")

    if book_found.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(403, f"You can only edit your own books")

    book_upd = await update_book(book_found, data.model_dump(), db)
    await invalidate_book(redis, book_id)
    return book_upd


@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                               db: Annotated[AsyncSession, Depends(get_db)],
                               current_user: Annotated[UserModel, Depends(get_current_active_user)],
                               redis: Annotated[Redis, Depends(get_redis)]
                               ):
    book_found = await get_one_book(book_id, db)

    if book_found is None:
        raise HTTPException(404, f"Book {book_id} not found")

    if book_found.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(403, f"Access denied")

    await delete_book(book_found, db)
    await invalidate_book(redis, book_id)
