from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.schemas.author import AuthorResponse


class CreateBook(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    author_id: Annotated[int, Field(ge=1)]
    price: Annotated[float, Field(ge=0)]
    description: Annotated[str | None, Field(max_length=1000)] = None


class AuthorBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author_id: int
    price: float
    description: str | None = None
    author: AuthorBrief | None = None