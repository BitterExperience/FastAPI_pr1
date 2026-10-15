from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm)


from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.crud.user import create_user_db, read_user_by_id_db, read_user_by_username_db
from app.security.password import verify_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/register')
async def create_user(data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    try:
        user = data.model_dump()
        return await create_user_db(user, db)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


# @router.post('/login')
# async def login_for_access_tokin(form_data: OAuth2PasswordRequestForm,
#                                  db: Annotated[AsyncSession, Depends(get_db)]) -> Token:
#     try:
#         user = await read_user_by_username_db(form_data.username, db)
#         if user is None or verify_password(form_data.password, user.hashed_password)
#             raise HTTPException(401, "Incorrect username or password")
#         password = verify_password(form_data.password, user.hashed_password)
#         return Token(access_token=password, token_type="bearer")
#     except ValueError as err:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err))


# @router.get("me/")
# async def read_users_me(current_user: Annotated[UserCreate, Depends(get_current_active_user)]) -> UserResponse:
#     return current_user
#



