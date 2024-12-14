from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import contextlib
import aiohttp

DATABASE_URL = "postgresql+asyncpg://crm3:Billkill13@postgres:5432/postgres"

# Создаем движок
engine = create_async_engine(DATABASE_URL, future=True)
# Создаем сессию
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

@contextlib.asynccontextmanager
async def get_db_session():
    """
    Контекстный менеджер для управления сессией базы данных.
    """
    try:
        session = AsyncSessionLocal()
        yield session
    finally:
        await session.close()
        await engine.dispose()

@contextlib.asynccontextmanager
async def get_http_session():
    """
    Контекстный менеджер для управления сессией aiohttp.
    """
    async with aiohttp.ClientSession() as session:
        try:
            yield session
        finally:
            await session.close()