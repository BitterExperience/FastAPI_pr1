from app.schemas.book import CreateBook, BookResponse, AuthorBrief
from app.schemas.author import CreateAuthor, AuthorResponse, BookBrief

#
# BookResponse.model_rebuild()
# AuthorResponse.model_rebuild()

__all__ = ["CreateBook", "BookResponse", "CreateAuthor", "AuthorResponse", "AuthorBrief", "BookBrief"]