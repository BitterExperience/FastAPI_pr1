from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Literal
from datetime import datetime


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=100)]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime

#
# class UserRoleUpdate(BaseModel):
#     role: Literal["user", "admin"]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
