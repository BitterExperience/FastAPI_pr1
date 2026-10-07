from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated



class CreateAuthor(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    bio: Annotated[str | None, Field(max_length=1000)] = None


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    bio: str | None = None