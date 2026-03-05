from fastapi import FastAPI

from src.exceptions import register_exception_handlers
from src.urls.router import router as urls_router

app = FastAPI(
    title="Short URL",
    description="Short URL API",
    version="1.0.0",
)

register_exception_handlers(app)
app.include_router(router=urls_router, tags=["URL"])
