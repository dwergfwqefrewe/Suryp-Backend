from models.comments import Comment
from schemas.comment import CommentUpdate
from .base_manager import BaseManager
from exceptions import DatabaseError


class CommentManager(BaseManager[Comment, CommentUpdate]):
    """
    Менеджер для работы с комментариями (асинхронный)
    """
    def __init__(self):
        super().__init__(Comment)

    async def create_obj(self, obj: Comment) -> Comment:
        try:
            return await super().create_obj(obj)
        except Exception as e:
            raise DatabaseError(f"Ошибка при создании комментария: {str(e)}")
