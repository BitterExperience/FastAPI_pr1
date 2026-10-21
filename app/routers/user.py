from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserResponse, Token
from app.crud.user import create_user_db, read_user_by_username_db, delete_user_db
from app.security.dependencies import get_current_active_user
from app.security.password import verify_password
from app.security.jwt import create_access_token



router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/register')
async def create_user(data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    try:
        user = data.model_dump()
        return await create_user_db(user, db)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.post('/login')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[AsyncSession, Depends(get_db)]) -> Token:

     user = await read_user_by_username_db(form_data.username, db)
     if user is None or not verify_password(form_data.password, user.hashed_password):
         raise HTTPException(401, "Incorrect username or password")
     access_token = create_access_token({"sub": str(user.id)})
     return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def read_users_me(current_user: Annotated[UserModel, Depends(get_current_active_user)]) -> UserResponse:
    return current_user


@router.delete("/me", status_code=204)
async def delete_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await delete_user_db(current_user, db)


# @router.delete("/{user_id}", status_code=204)
# async def user_delete(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
#     user_find = await read_user_by_id_db(user_id, db)
#     if user_find is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#
#     await delete_user_by_id_db(user_id, db)
#     return f"User {user_find.username} delete"


