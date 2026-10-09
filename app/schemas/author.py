from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.schemas.book import BookResponse


class CreateAuthor(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    bio: Annotated[str | None, Field(max_length=1000)] = None


class BookBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    price: float


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    bio: str | None = None
    books: list[BookBrief] | None = None