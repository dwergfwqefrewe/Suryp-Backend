from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from exceptions.histories import HistoryNotFoundError
from database.managers.base_manager import BaseManager
from database.models.history import History
from schemas.history import HistoryUpdate, HistoryOut, HistoryOutShort
from exceptions.base import DatabaseError

from core.logger import app_logger

class HistoryManager(BaseManager[History, HistoryUpdate]):
    """
    Менеджер для работы с историями (асинхронный)
    """
    def __init__(self) -> None:
        super().__init__(History)

    async def _get_history_by_id(self, id: int) -> Optional[History]:
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model).where(self._model.id == id)
            )
                return result.scalars().first()
        except Exception as e:
            app_logger.exception(f"История с id {id} не найдена")
            raise DatabaseError(f"История с id {id} не найдена")

    async def _get_histories_by_author_id(self, author_id: int) -> List[History]:
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model).where(self._model.author_id == author_id)
            )
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Истории с author_id {author_id} не найдены")
            raise DatabaseError(f"Истории с author_id {author_id} не найдены")

    async def get_histories_with_authors(self) -> List[HistoryOut]:
        """
        Получение всех историй с авторами (асинхронно)
        """
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model).options(joinedload(self._model.author))
                )
                histories = result.scalars().all()
                return [HistoryOut.model_validate(history) for history in histories]
        except Exception as e:
            app_logger.exception(f"Ошибка при получении историй")
            raise DatabaseError(f"Ошибка при получении историй")

    async def get_histories_by_author_id(self, author_id: int, skip: int = 0, limit: int = 100) -> List[HistoryOutShort]:
        """
        Получение всех историй конкретного пользователя (асинхронно)
        """
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model)
                    .where(self._model.author_id == author_id)
                    .offset(skip)
                    .limit(limit)
                )
                histories = result.scalars().all()
                return [HistoryOutShort.model_validate(h) for h in histories] if histories else []
        except Exception as e:
            app_logger.exception(f"Ошибка при получении историй пользователя {author_id}")
            raise DatabaseError(f"Ошибка при получении историй пользователя {author_id}")

    async def get_history_by_id_with_author(self, id: int) -> HistoryOut | None:
        """
        Получение истории по id с автором (асинхронно)
        """
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model).options(joinedload(self._model.author)).where(self._model.id == id)
                )
                history = result.scalars().first()
                if not history:
                    return None
                return HistoryOut.model_validate(history)
        except Exception as e:
            app_logger.exception(f"Ошибка при получении истории {id}")
            raise DatabaseError(f"Ошибка при получении истории {id}")

    async def create_history_with_response(self, history_obj: History) -> HistoryOut:
        """
        Создать историю и вернуть сериализованный HistoryOut с автором (асинхронно)
        """
        try:
            async with self.manager.get_async_session() as session:
                session.add(history_obj)
                await session.commit()
                result = await session.execute(
                    select(self._model).options(joinedload(self._model.author)).where(self._model.id == history_obj.id)
                )
                history_with_author = result.scalars().first()
                return HistoryOut.model_validate(history_with_author)
        except Exception as e:
            app_logger.exception(f"Ошибка при создании истории")
            raise DatabaseError(f"Ошибка при создании истории") 

    async def delete_history_with_response(self, id: int) -> HistoryOut:
        """
        Удалить историю и вернуть сериализованный HistoryOut с автором (асинхронно)
        """
        try:
            async with self.manager.get_async_session() as session:
                result = await session.execute(
                    select(self._model).options(joinedload(self._model.author)).where(self._model.id == id)
                )
                history = result.scalars().first()
                if not history:
                    raise HistoryNotFoundError()
                await session.delete(history)
                await session.commit()
                return HistoryOut.model_validate(history)
        except Exception as e:
            app_logger.exception(f"Ошибка при удалении истории {id}")
            raise DatabaseError(f"Ошибка при удалении истории {id}")
