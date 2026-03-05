from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from src.urls import schemas as urls_schemas
from src.urls.dependencies import get_url_service
from src.urls.service import URLService

router = APIRouter()


@router.post("/shorten", response_model=urls_schemas.URLCreateResponse)
async def shorten_url(
        data: urls_schemas.URLCreateRequest,
        service: URLService = Depends(get_url_service),
):
    return await service.create_url(str(data.original_url))


@router.get("/{short_code}")
async def redirect_url(
        short_code: str,
        service: URLService = Depends(get_url_service),
):
    url = await service.get_url(short_code)
    await service.record_click(url.id)
    return RedirectResponse(url=url.original_url)


@router.get("/stats/{short_code}", response_model=urls_schemas.URLStatsResponse)
async def get_stats(
        short_code: str,
        service: URLService = Depends(get_url_service),
):
    url = await service.get_url(short_code)
    return urls_schemas.URLStatsResponse(clicks=url.clicks)
