from abc import ABC
from collections.abc import Sequence
from typing import Generic, TypeVar, Type, Optional, List
from pydantic import BaseModel

from database.managers.session_manager import Manager
from exceptions import DatabaseError

TModel = TypeVar('TModel')
TUpdate = TypeVar('TUpdate', bound=BaseModel)


class BaseManager(ABC, Generic[TModel, TUpdate]):
    """Базовый менеджер для работы с моделями"""

    def __init__(self, model: Type[TModel]) -> None:
        self._model = model
        self.manager = Manager()


    def get_obj_by_id(self, id: int, options: Optional[List] = None) -> Optional[TModel]:
        """Получение объекта по id с опциями
            - id - id объекта
            - options - опции для запроса
        """
        if options is None:
            options = []
            
        try:
            with self.manager.get_session() as session:
                query = session.query(self._model)

                if options:
                    for option in options:
                        query = query.options(option)

                obj = query.filter(self._model.id == id).first()
                return obj
        except Exception as e:
            raise DatabaseError(f"Ошибка при получении объекта: {str(e)}")


    def get_all_obj(self,
                    options: Optional[List] = None,
                    skip: int = 0,
                    limit: int = 100) -> Sequence[TModel]:
        """Получение всех объектов с опциями и пагинацией
            - options - опции для запроса
            - skip - количество объектов, которые нужно пропустить
            - limit - количество объектов, которые нужно получить
        """
        if options is None:
            options = []
            
        try:
            with self.manager.get_session() as session:
                query = session.query(self._model)

                if options:
                    for option in options:
                        query = query.options(option)

                return query.offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseError(f"Ошибка при получении объектов: {str(e)}")


    def create_obj(self, obj: TModel) -> TModel:
        """Создание объекта
            - obj - объект для создания
        """
        with self.manager.get_session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)

            return obj
        

    def delete_obj(self, id: int) -> TModel | None:
        """Удаление объекта по id
            - id - id объекта
        """
        with self.manager.get_session() as session:
            obj = session.get(self._model, int(id))
            if not obj:
                return None

            session.delete(obj)
            session.commit()

            return obj
        
        
    def update_obj(self, id: int, updated_obj: TUpdate) -> TModel | None:
        """Обновление объекта по id
            - id - id объекта
            - updated_obj - обновленный объект
        """
        with self.manager.get_session() as session:
            obj = session.get(self._model, int(id))

            if not obj:
                return None

            data = updated_obj.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != 'id':
                    setattr(obj, key, value)

            session.commit()
            session.refresh(obj)

            return obj
