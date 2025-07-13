from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import settings
from core.logger import app_logger

engine = create_async_engine(
    url=settings.database_url, 
    echo=settings.debug,
    pool_pre_ping=True,
)

app_logger.info(f"Создан движок базы данных {settings.database_url}")

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

app_logger.info(f"Создана асинхронная сессия базы данных")

Base = declarative_base()
