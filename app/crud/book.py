
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models import BookModel


async def create_book(data_book: dict, db: AsyncSession)  -> BookModel:
    book = BookModel(**data_book)
    db.add(book)
    await db.commit()
    await db.refresh(book)

    return book


async def get_all_books(db: AsyncSession) -> list[BookModel]:
    stmt = select(BookModel)
    result = await db.execute(stmt)
    books = result.scalars().all()

    return books


async def get_one_book(id_book: int,
                       db: AsyncSession) -> BookModel | None:

    stmt = select(BookModel).where(BookModel.id==id_book)
    result = await db.execute(stmt)
    book = result.scalar_one_or_none()


    return book


async def update_book(book: BookModel,
                      data: dict,
                      db: AsyncSession) -> BookModel:

    for key, val in data.items():
        setattr(book, key, val)

    await db.commit()

    return book


async def delete_book(book: BookModel,
                         db: AsyncSession):


    await db.delete(book)
    await db.commit()


