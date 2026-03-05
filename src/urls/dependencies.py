from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_postgres
from src.urls.repository import URLRepository
from src.urls.service import URLService


async def get_url_repository(
        session: AsyncSession = Depends(get_postgres),
) -> URLRepository:
    return URLRepository(session)


async def get_url_service(
        repository: URLRepository = Depends(get_url_repository),
) -> URLService:
    return URLService(repository)