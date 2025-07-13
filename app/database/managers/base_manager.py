from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar, Type, Optional, List

from pydantic import BaseModel
from sqlalchemy.future import select

from database.managers.session_manager import Manager
from exceptions.base import DatabaseError, ModelNotFoundError
from core.logger import app_logger

TModel = TypeVar('TModel')
TUpdate = TypeVar('TUpdate', bound=BaseModel)


class BaseManager(ABC, Generic[TModel, TUpdate]):
    """Базовый менеджер для работы с моделями (асинхронный)"""

    def __init__(self, model: Type[TModel]) -> None:
        self._model = model
        self.manager = Manager()

    async def create_obj(self, obj: TModel) -> TModel:
        """Создание объекта (асинхронно)"""
        async with self.manager.get_async_session() as session:
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except Exception as e:
                await session.rollback()
                app_logger.exception(f"{self._model.__name__} не создан Traceback: {e.__traceback__}")
                raise DatabaseError

    async def get_obj_by_id(self, id: int, options: Optional[List] = None) -> TModel:
        """Получение объекта по id с опциями (асинхронно)"""
        if options is None:
            options = []
        try:
            async with self.manager.get_async_session() as session:
                query = select(self._model)
                for option in options:
                    query = query.options(option)
                result = await session.execute(
                    query.where(getattr(self._model, "id") == id)
                )
                obj = result.scalars().first()
                if not obj:
                    app_logger.error(f"{self._model.__name__} с id {id} не найден")
                    raise ModelNotFoundError(f"{self._model.__name__} с id {id} не найден")
                return obj
        except Exception as e:
            app_logger.exception(f"{self._model.__name__} с id {id} не найден Traceback: {e.__traceback__}")
            raise DatabaseError

    async def get_all_obj(self,
                          options: Optional[List] = None,
                          skip: int = 0,
                          limit: int = 100) -> Sequence[TModel]:
        """Получение всех объектов с опциями и пагинацией (асинхронно)"""
        if options is None:
            options = []
        try:
            async with self.manager.get_async_session() as session:
                query = select(self._model)
                for option in options:
                    query = query.options(option)
                query = query.offset(skip).limit(limit)
                result = await session.execute(query)
                if not result.scalars().all():
                    app_logger.error(f"{self._model.__name__} не найдены")
                    raise ModelNotFoundError(f"{self._model.__name__} не найдены")
                return result.scalars().all()
        except Exception as e:
            app_logger.exception(f"{self._model.__name__} не найдены Traceback: {e.__traceback__}")
            raise DatabaseError

    async def update_obj(self, id: int, updated_obj: TUpdate) -> TModel:
        """Обновление объекта по id (асинхронно)"""
        async with self.manager.get_async_session() as session:
            obj = await session.get(self._model, int(id))
            if not obj:
                app_logger.error(f"{self._model.__name__} с id {id} не найден")
                raise ModelNotFoundError(f"{self._model.__name__} с id {id} не найден")
            data = updated_obj.model_dump(exclude_unset=True)
            for key, value in data.items():
                if key != 'id':
                    setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def delete_obj(self, id: int) -> TModel:
        """Удаление объекта по id (асинхронно)"""
        async with self.manager.get_async_session() as session:
            obj = await session.get(self._model, int(id))
            if not obj:
                app_logger.error(f"{self._model.__name__} с id {id} не найден")
                raise ModelNotFoundError(f"{self._model.__name__} с id {id} не найден")
            await session.delete(obj)
            await session.commit()
            return obj
