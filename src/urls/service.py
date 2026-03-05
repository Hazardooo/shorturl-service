import secrets
import string
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.urls.exceptions import URLCollisionError, URLNotFound
from src.urls.models import URL
from src.urls.repository import URLRepository
from src.urls.schemas import URLCreateResponse


@dataclass(slots=True)
class URLService:
    repository: URLRepository

    async def create_url(self, original_url: str) -> URLCreateResponse:
        for _ in range(3):
            short_id = self._generate_short_id()
            try:
                url = await self.repository.create(original_url, short_id)
                return URLCreateResponse(
                    short_id=f"/{short_id}",
                    original_url=url.original_url,
                )
            except IntegrityError:
                continue
        raise URLCollisionError()

    async def get_url(self, short_id: str) -> URL | None:
        url = await self.repository.get_by_short_id(short_id)
        if not url:
            raise URLNotFound()
        return url

    async def record_click(self, url_id: UUID) -> None:
        await self.repository.increment_clicks(url_id)

    @staticmethod
    def _generate_short_id(length: int = 6) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
