from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://crm3:Billkill13@postgres:5432/postgres"

# Создаем движок
engine = create_async_engine(DATABASE_URL, future=True)
# Создаем сессию
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()