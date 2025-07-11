from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar, Type, Optional, List
from pydantic import BaseModel

from database.managers.session_manager import Manager
from exceptions import DatabaseError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

TModel = TypeVar('TModel')
TUpdate = TypeVar('TUpdate', bound=BaseModel)


class BaseManager(ABC, Generic[TModel, TUpdate]):
    """Базовый менеджер для работы с моделями (асинхронный)"""

    def __init__(self, model: Type[TModel]) -> None:
        self._model = model
        self.manager = Manager()

    async def get_obj_by_id(self, id: int, options: Optional[List] = None) -> Optional[TModel]:
        """Получение объекта по id с опциями (асинхронно)"""
        if options is None:
            options = []
        try:
            async with self.manager.get_async_session() as session:
                query = select(self._model)
                for option in options:
                    query = query.options(option)
                result = await session.execute(query.where(self._model.id == id))
                obj = result.scalars().first()
                return obj
        except Exception as e:
            raise DatabaseError(f"Ошибка при получении объекта: {str(e)}")

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
                return result.scalars().all()
        except Exception as e:
            raise DatabaseError(f"Ошибка при получении объектов: {str(e)}")

    async def create_obj(self, obj: TModel) -> TModel:
        """Создание объекта (асинхронно)"""
        async with self.manager.get_async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def delete_obj(self, id: int) -> TModel | None:
        """Удаление объекта по id (асинхронно)"""
        async with self.manager.get_async_session() as session:
            obj = await session.get(self._model, int(id))
            if not obj:
                return None
            await session.delete(obj)
            await session.commit()
            return obj

    async def update_obj(self, id: int, updated_obj: TUpdate) -> TModel | None:
        """Обновление объекта по id (асинхронно)"""
        async with self.manager.get_async_session() as session:
            obj = await session.get(self._model, int(id))
            if not obj:
                return None
            data = updated_obj.model_dump(exclude_unset=True)
            for key, value in data.items():
                if key != 'id':
                    setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
            return obj
