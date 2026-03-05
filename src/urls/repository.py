from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.urls.models import URL


class URLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, original_url: str, short_id: str) -> URL:
        url = URL(original_url=original_url, short_id=short_id)
        self.session.add(url)
        await self.session.flush()
        return url

    async def get_by_short_id(self, short_id: str) -> URL | None:
        result = await self.session.execute(
            select(URL).where(URL.short_id == short_id)
        )
        return result.scalar_one_or_none()

    async def increment_clicks(self, url_id: UUID) -> None:
        await self.session.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(clicks=URL.clicks + 1)
        )
