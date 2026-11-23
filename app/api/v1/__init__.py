from fastapi import APIRouter

from app.api.v1.routers.book import router as book_router
from app.api.v1.routers.author import router as author_router
from app.api.v1.routers.user import router as user_router
from app.api.v1.routers.admin import router as admin_router

router = APIRouter(prefix="/v1")

router.include_router(book_router, prefix="/books")
router.include_router(author_router, prefix="/authors")
router.include_router(user_router, prefix="/users")
router.include_router(admin_router, prefix="/admin")