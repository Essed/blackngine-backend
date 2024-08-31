from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import settings as settings


engine = create_async_engine(settings.DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()