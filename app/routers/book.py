
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from app.schemas import CreateBook, BookResponse
from app.db.session import get_db
from app.crud import create_book, get_one_book, get_all_books, update_book, delete_book


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", status_code=201)
async def create_book_endpoint(data: CreateBook, db: Annotated[AsyncSession, Depends(get_db)])  -> BookResponse:
    data_book = data.model_dump()
    return await create_book(data_book, db)


@router.get("")
async def get_all_endpoint(db: Annotated[AsyncSession, Depends(get_db)]) -> list[BookResponse]:
    return await get_all_books(db)


@router.get("/{book_id}")
async def get_one_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                       db: Annotated[AsyncSession, Depends(get_db)]) -> BookResponse:

    book = await get_one_book(book_id, db)

    if book is None:
        raise HTTPException(404, f"Book {book_id} not found")

    return book


@router.put("/{book_id}", status_code=200)
async def update_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                      data: CreateBook,
                      db: Annotated[AsyncSession, Depends(get_db)]) -> BookResponse:

    book_found = await get_one_book(book_id, db)


    if book_found is None:
        raise HTTPException(404, f"Book {book_id} not found")

    book_upd = await update_book(book_found, data.model_dump(), db)
    return book_upd


@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(book_id: Annotated[int, Path(ge=1)],
                         db: Annotated[AsyncSession, Depends(get_db)]):

    book_found = await get_one_book(book_id, db)


    if book_found is None:
        raise HTTPException(404, f"Book {book_id} not found")

    await delete_book(book_found, db)
