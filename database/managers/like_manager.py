from models.history_like import HistoryLike
from schemas.like import LikeUpdate
from .base_manager import BaseManager
from exceptions import DatabaseError


class LikeManager(BaseManager[HistoryLike, LikeUpdate]):
    """
    Менеджер для работы с лайками (асинхронный)
    """
    def __init__(self):
        super().__init__(HistoryLike)

    async def create_obj(self, obj: HistoryLike) -> HistoryLike:
        try:
            return await super().create_obj(obj)
        except Exception as e:
            raise DatabaseError(f"Ошибка при создании лайка: {str(e)}")
