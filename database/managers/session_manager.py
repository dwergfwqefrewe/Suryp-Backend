from typing import Any, Generator, Self
from contextlib import contextmanager

from sqlalchemy.orm import Session

from database.config import engine, Base, SessionLocal


class Manager:
    """Менеджер для работы с сессиями базы данных
        - _instance - экземпляр менеджера
        - SessionLocal - сессия базы данных
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
        self.SessionLocal = SessionLocal
        self.engine = engine

        Base.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, Any, None]:
        """Контекстный менеджер для работы с session SQLAlchemy"""
        session = self.SessionLocal()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


manager: Manager = Manager()
