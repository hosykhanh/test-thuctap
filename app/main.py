from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import user_router, post_router, comment_router, like_router
from .core.create_db import create_database

create_database()

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Thêm cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các domain truy cập API
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các header
)

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
app.include_router(comment_router.router, prefix="/comments", tags=["Comments"])
app.include_router(like_router.router, prefix="/likes", tags=["Likes"])
