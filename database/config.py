from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from main_config import settings

# Создаем движок базы данных
engine = create_engine(
    url=settings.database_url,
    echo=settings.debug,  # Логирование SQL запросов в debug режиме
    pool_pre_ping=True,   # Проверка соединения перед использованием
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)
