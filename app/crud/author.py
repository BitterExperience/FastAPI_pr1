
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from app.models.author import AuthorModel




async def create_author_db(data: dict, db: AsyncSession) -> AuthorModel:
    author = AuthorModel(**data)
    stmt_name = select(AuthorModel).where(AuthorModel.name==author.name)
    res_stmt_name = await db.execute(stmt_name)
    name_existing = res_stmt_name.scalar_one_or_none()
    if name_existing is not None:
            raise ValueError(f"Author {author.name} already exists")
    try:
        db.add(author)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"Author {author.name} already exists")
    stmt = select(AuthorModel).where(AuthorModel.id==author.id).options(selectinload(AuthorModel.books))
    result = await db.execute(stmt)
    author_create =  result.scalar_one_or_none()
    return author_create


async def read_author_db(author_id: int, db: AsyncSession) -> AuthorModel | None:
    stmt = select(AuthorModel).where(AuthorModel.id==author_id).options(selectinload(AuthorModel.books))
    result = await db.execute(stmt)
    author =  result.scalar_one_or_none()

    return author


async def read_all_authors_db(db: AsyncSession) -> list[AuthorModel]:
    stmt = select(AuthorModel).options(selectinload(AuthorModel.books))
    result =  await db.execute(stmt)
    authors = result.scalars().all()
    return authors


async def update_author_db(author: AuthorModel, data: dict, db: AsyncSession) -> AuthorModel:

    for k, v in data.items():
        setattr(author, k, v)

    await db.commit()

    return author

async def delete_author_db(author: AuthorModel, db: AsyncSession) -> None:
    await db.delete(author)
    await db.commit()

    return None