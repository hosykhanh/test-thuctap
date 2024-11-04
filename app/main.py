from fastapi import FastAPI
from .config import settings
from .routers import items

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Thêm các route từ items
app.include_router(items.router, prefix="/api")
