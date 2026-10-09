from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.author import (create_author_db,
                             read_author_db,
                             read_all_authors_db, update_author_db, delete_author_db)
from app.db.session import get_db
from app.schemas.author import CreateAuthor, AuthorResponse

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post('', status_code=201) 
async def create_author(data: CreateAuthor, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorResponse:
    try:
        author = data.model_dump()
        return await create_author_db(author, db)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(err))

@router.get('/{author_id}')
async def get_author(author_id: Annotated[int, Path(ge=1)], db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorResponse:
    author = await read_author_db(author_id, db)
    if author is None:
        raise HTTPException(404, f"Author {author_id} not found")

    return author


@router.get('')
async def get_all_authors(db: Annotated[AsyncSession, Depends(get_db)]) -> list[AuthorResponse]:
    return await read_all_authors_db(db)


@router.put('/{author_id}')
async def update_author(author_id: Annotated[int, Path(ge=1)], data: CreateAuthor, db: Annotated[AsyncSession, Depends(get_db)]) -> AuthorResponse:
    author_found = await read_author_db(author_id, db)
    if author_found is None:
        raise HTTPException(404, f"Author {author_id} not found")

    upd_author = await update_author_db(author_found, data.model_dump(), db)

    return upd_author

@router.delete('/{author_id}', status_code=204)
async def delete_author(author_id: Annotated[int, Path(ge=1)], db: Annotated[AsyncSession, Depends(get_db)]):
    author_found = await read_author_db(author_id, db)

    if author_found is None:
        raise HTTPException(404, f"Author {author_id} not found")

    await delete_author_db(author_found, db)