from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base



class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str | None] = mapped_column(String(1000))

    books: Mapped[list["BookModel"]] = relationship(back_populates="author", cascade="all, delete-orphan")
