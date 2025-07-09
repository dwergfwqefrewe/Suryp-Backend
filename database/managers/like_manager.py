from models.history_like import HistoryLike
from schemas.like import LikeUpdate
from .base_manager import BaseManager


class LikeManager(BaseManager[HistoryLike, LikeUpdate]):
    """Менеджер для работы с лайками"""

    def __init__(self):
        super().__init__(HistoryLike)
