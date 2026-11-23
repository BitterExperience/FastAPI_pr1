from app.api.v1.routers.book import router as book_router
from app.api.v1.routers.author import router as author_router
from app.api.v1.routers.user import router as user_router
from app.api.v1.routers.admin import router as admin_router


__all__ = ["book_router", "author_router", "user_router", "admin_router"]
