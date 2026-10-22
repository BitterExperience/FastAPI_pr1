from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import read_user_by_id_db
from app.db.session import get_db
from app.models.user import UserModel
from app.security.jwt import decode_access_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_schema)],
                           db: Annotated[AsyncSession, Depends(get_db)]) -> UserModel:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        user_id = int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_active_user(current_user: Annotated[UserModel, Depends(get_current_user)]) -> UserModel:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return current_user


async def get_current_admin(current_user: Annotated[UserModel, Depends(get_current_active_user)]) -> UserModel:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return current_user