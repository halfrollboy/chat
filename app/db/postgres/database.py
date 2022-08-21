from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from .dependencies import get_db_settings

settings = get_db_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=50, echo=True
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Model = declarative_base()
