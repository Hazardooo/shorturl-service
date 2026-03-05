from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.urls.exceptions import URLNotFound, URLCollisionError


class HTTPExceptionResponse(JSONResponse):
    def __init__(self, status_code: int, error_code: str, message: str):
        super().__init__(
            status_code=status_code,
            content={"error": error_code, "message": message}
        )


async def url_not_found_handler(request: Request, exc: URLNotFound) -> HTTPExceptionResponse:
    return HTTPExceptionResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="URL_NOT_FOUND",
        message="Short ID not found"
    )


async def url_collision_handler(request: Request, exc: URLCollisionError) -> HTTPExceptionResponse:
    return HTTPExceptionResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="URL_GENERATION_FAILED",
        message="Failed to generate unique short id"
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> HTTPExceptionResponse:
    return HTTPExceptionResponse(
        status_code=status.HTTP_409_CONFLICT,
        error_code="RESOURCE_CONFLICT",
        message="Resource already exists or constraint violation"
    )


def register_exception_handlers(app):
    app.add_exception_handler(URLNotFound, url_not_found_handler)
    app.add_exception_handler(URLCollisionError, url_collision_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
