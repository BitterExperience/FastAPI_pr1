from app.routers.book import router as book_router
from app.routers.author import router as author_router
from app.routers.user import router as user_router


__all__ = ["book_router", "author_router", "user_router"]