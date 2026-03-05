from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import app_config


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    app_config.POSTGRES_URL,
    pool_pre_ping=True,
    echo=False,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    connect_args={
        "command_timeout": 60,
        "server_settings": {"application_name": "shorturl"},
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()


async def get_postgres() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_session() as session:
        yield session
