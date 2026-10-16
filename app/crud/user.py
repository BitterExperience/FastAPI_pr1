from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.user import UserModel
from app.security.password import hash_password


async def create_user_db(data: dict, db: AsyncSession) -> UserModel:

    stmt_name = select(UserModel).where(UserModel.username == data["username"])
    exec_name = await db.execute(stmt_name)
    res_name = exec_name.scalar_one_or_none()
    if res_name:
        raise ValueError(f"User {data['username']} already exists")

    stmt_email = select(UserModel).where(UserModel.email == data["email"])
    exec_email = await db.execute(stmt_email)
    res_email = exec_email.scalar_one_or_none()
    if res_email:
        raise ValueError(f"Email {data['email']} already exists")

    data = data.copy()
    user_password = data.pop("password")
    hashed_password = hash_password(user_password)
    data["hashed_password"] = hashed_password
    user = UserModel(**data)

    try:
        db.add(user)
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ValueError(f"User {data['username']} already exists")

    await db.refresh(user)
    return user


async def read_user_by_id_db(user_id: int, db: AsyncSession) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def read_user_by_username_db(username: str, db: AsyncSession) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.username == username)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


