from models.comments import Comment
from schemas.comment import CommentUpdate
from .base_manager import BaseManager


class CommentManager(BaseManager[Comment, CommentUpdate]):
    """Менеджер для работы с комментариями"""

    def __init__(self):
        super().__init__(Comment)
