from uuid import UUID

from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    original_url: str
    short_id: str
    clicks: int


class URLSchema(URLBase):
    id: UUID

    class Config:
        from_attributes = True


class URLCreateRequest(BaseModel):
    original_url: HttpUrl


class URLCreateResponse(BaseModel):
    original_url: str
    short_id: str

    class Config:
        from_attributes = True


class URLStatsResponse(BaseModel):
    clicks: int
