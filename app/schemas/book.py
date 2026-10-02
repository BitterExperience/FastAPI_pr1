from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated



class CreateBook(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    author: Annotated[str, Field(min_length=2, max_length=100)]
    price: Annotated[float, Field(ge=0)]
    description: Annotated[str | None, Field(max_length=1000)] = None



class BookResponse(CreateBook):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    price: float
    description: str | None = None