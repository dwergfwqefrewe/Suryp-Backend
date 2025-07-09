from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

# Создаем движок базы данных
engine = create_engine(
    url=settings.database_url,
    echo=settings.debug,  # Логирование SQL запросов в debug режиме
    pool_pre_ping=True,   # Проверка соединения перед использованием
)

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)
