from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.models.user import UserModel
from app.schemas.user import UserResponse
from app.security.dependencies import get_current_admin
from app.db.session import get_db

from app.crud.user import read_user_by_id_db, delete_user_db, read_all_users, update_user_db

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", status_code=200)
async def get_admin(
        _admin: Annotated[UserModel, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: Annotated[int, Query(ge=0, description="Сколько пропускать")] = 0,
        limit: Annotated[int, Query(ge=1, le=100, description="Сколько вернуть")] = 20

) -> list[UserResponse]:
    return await read_all_users(skip, limit, db)


@router.patch("/users/{user_id}/block", status_code=200)
async def block_user(user_id: Annotated[int, Path(ge=1)],
                     _admin: Annotated[UserModel, Depends(get_current_admin)],
                     db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(404, detail="User not found")
    if user_id == _admin.id:
        raise HTTPException(400, "You cannot block yourself")
    user_upd = await update_user_db(user, {"is_active": False}, db)
    return user_upd


@router.patch("/users/{user_id}/unblock", status_code=200)
async def unblock_user(user_id: Annotated[int, Path(ge=1)],
                       _admin: Annotated[UserModel, Depends(get_current_admin)],
                       db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(404, detail="User not found")
    if user_id == _admin.id:
        raise HTTPException(400, "You cannot unblock yourself")
    user_upd = await update_user_db(user, {"is_active": True}, db)
    return user_upd


@router.patch("/users/{user_id}/make-admin", status_code=200)
async def make_admin(user_id: Annotated[int, Path(ge=1)],
                     _admin: Annotated[UserModel, Depends(get_current_admin)],
                     db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(404, detail="User not found")
    if user_id == _admin.id:
        raise HTTPException(400, "You cannot update yourself")
    return await update_user_db(user, {"role": "admin"}, db)


@router.patch("/users/{user_id}/make_user_instead_admin", status_code=200)
async def make_user_instead_admin(user_id: Annotated[int, Path(ge=1)],
                                  _admin: Annotated[UserModel, Depends(get_current_admin)],
                                  db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(404, detail="User not found")
    if user_id == _admin.id:
        raise HTTPException(400, "You cannot update yourself")
    return await update_user_db(user, {"role": "user"}, db)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: Annotated[int, Path(ge=1)],
                      _admin: Annotated[UserModel, Depends(get_current_admin)],
                      db: Annotated[AsyncSession, Depends(get_db)]):
    user = await read_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(404, detail="User not found")
    if user_id == _admin.id:
        raise HTTPException(400, "You cannot delete yourself")
    await delete_user_db(user, db)

