from typing import List

from sqlalchemy.orm import joinedload

from database.managers.base_manager import BaseManager
from models.history import History
from schemas.history import HistoryUpdate, HistoryOut, HistoryOutShort


class HistoryManager(BaseManager[History, HistoryUpdate]):
    """Менеджер для работы с историями"""

    def __init__(self) -> None:
        super().__init__(History)

    def get_histories_with_authors(self) -> List[HistoryOut]:
        """Получение всех историй с авторами"""
        with self.manager.get_session() as session:
            query = session.query(self._model).options(joinedload(self._model.author))
            histories = query.all()
            return [HistoryOut.model_validate(history) for history in histories]

    def get_histories_by_author_id(self, author_id: int) -> List[HistoryOutShort] | []:
        """Получение всех историй конкретного пользователя"""
        with self.manager.get_session() as session:
            histories = session.query(self._model)\
                .filter(self._model.author_id == author_id).all()
            if not histories:
                return []
            return [HistoryOutShort.model_validate(h) for h in histories]

    def get_history_by_id_with_author(self, id: int) -> HistoryOut | None:
        """Получение истории по id с автором"""
        with self.manager.get_session() as session:
            query = session.query(self._model).options(joinedload(self._model.author))
            history = query.get(id)
            if not history:
                return None
            return history

    def create_history_with_response(self, history_obj) -> HistoryOut:
        """Создать историю и вернуть сериализованный HistoryOut с автором"""
        with self.manager.get_session() as session:
            session.add(history_obj)
            session.commit()
            history_with_author = session.query(self._model).options(joinedload(self._model.author)).get(history_obj.id)
            return HistoryOut.model_validate(history_with_author) 

    def delete_history_with_response(self, id: int) -> HistoryOut | None:
        """Удалить историю и вернуть сериализованный HistoryOut с автором"""
        with self.manager.get_session() as session:
            history = session.query(self._model).options(joinedload(self._model.author)).get(id)
            if not history:
                return None
            session.delete(history)
            session.commit()
            return HistoryOut.model_validate(history)
