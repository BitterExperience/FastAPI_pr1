from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.author import AuthorModel


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]  = mapped_column(String(200))
    author: Mapped[AuthorModel] = relationship(back_populates='books')
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str | None] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))


