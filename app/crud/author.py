from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



from app.models.author import AuthorModel




async def create_author_db(data: dict, db: AsyncSession) -> AuthorModel:
    author = AuthorModel(**data)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


async def read_author_db(author_id: int, db: AsyncSession) -> AuthorModel | None:
    stmt = select(AuthorModel).where(AuthorModel.id==author_id)
    result = await db.execute(stmt)
    author =  result.scalar_one_or_none()

    return author


async def read_all_authors_db(db: AsyncSession) -> list[AuthorModel]:
    stmt = select(AuthorModel)
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