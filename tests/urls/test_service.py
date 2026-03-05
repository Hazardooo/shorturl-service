from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from src.urls.exceptions import URLCollisionError
from src.urls.service import URLService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def url_service(mock_repository):
    return URLService(repository=mock_repository)


class TestURLService:

    @pytest.mark.asyncio
    async def test_create_url_success(self, url_service, mock_repository):
        original_url = "https://example.com/long/path"
        mock_url = MagicMock()
        mock_url.original_url = original_url
        mock_repository.create.return_value = mock_url
        result = await url_service.create_url(original_url)
        assert result.original_url == original_url
        assert result.short_id.startswith("/")
        assert len(result.short_id) == 7
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_url_collision_then_success(self, url_service, mock_repository):
        original_url = "https://example.com"
        mock_repository.create.side_effect = [
            IntegrityError("duplicate", "short_id", Exception()),
            MagicMock(original_url=original_url)
        ]
        result = await url_service.create_url(original_url)
        assert result.original_url == original_url
        assert mock_repository.create.call_count == 2

    @pytest.mark.asyncio
    async def test_create_url_all_attempts_fail(self, url_service, mock_repository):
        original_url = "https://example.com"
        mock_repository.create.side_effect = IntegrityError("dup", "sc", Exception())
        with pytest.raises(URLCollisionError):
            await url_service.create_url(original_url)
        assert mock_repository.create.call_count == 3
