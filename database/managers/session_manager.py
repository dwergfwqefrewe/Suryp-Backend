from typing import Any, Generator, Self, AsyncGenerator
from contextlib import contextmanager, asynccontextmanager

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import engine, Base, AsyncSessionLocal


class Manager:
    """
    Менеджер для работы с сессиями базы данных
        - _instance - экземпляр менеджера
        - AsyncSessionLocal - асинхронная сессия базы данных
        - engine - движок базы данных
    """

    _instance = None

    def __new__(cls) -> Self:
        """Создание экземпляра менеджера"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Инициализация менеджера"""
        self.AsyncSessionLocal = AsyncSessionLocal
        self.engine = engine

    @contextmanager
    def get_session(self) -> Generator[Session, Any, None]:
        """Контекстный менеджер для работы с session SQLAlchemy (заглушка)"""
        raise NotImplementedError('Синхронная сессия не реализована, используйте get_async_session')

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """Асинхронный контекстный менеджер для работы с AsyncSession SQLAlchemy"""
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


manager: Manager = Manager()
