from database.models.user import User
from database.models.comments import Comment
from database.models.history import History
from database.models.history_like import HistoryLike

from database.managers.comment_manager import CommentManager
from database.managers.history_manager import HistoryManager
from database.managers.like_manager import LikeManager

from core.logger import app_logger

from exceptions.comment import CommentNotFoundError, OwnershipCommentError
from exceptions.histories import HistoryNotFoundError, OwnershipHistoryError
from exceptions.like import LikeNotFoundError, OwnershipLikeError
from exceptions.users import UserNotFoundError

comment_manager = CommentManager()
history_manager = HistoryManager()
like_manager = LikeManager()


async def get_comment_or_error(id: int, user: User) -> Comment:
    """
    Получает комментарий из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    comment = await comment_manager.get_obj_by_id(id=id)
    if not comment:
        app_logger.error(f"Комментарий {id} не найден")
        raise CommentNotFoundError()
    user_id = getattr(comment, 'user_id', None)
    if user_id is None:
        app_logger.error(f"Пользователь {user_id} не найден")
        raise UserNotFoundError()
    if user_id != user.id:
        app_logger.warning(f"Пользователь {user.id} попытался получить доступ к комментарию {id}")
        raise OwnershipCommentError()
    return comment


async def get_history_or_error(id: int, user: User) -> History:
    """
    Получает историю из БД по ID и проверяет, что она принадлежит текущему пользователю
    """
    history = await history_manager.get_obj_by_id(id=id)
    if not history:
        app_logger.error(f"История {id} не найдена")
        raise HistoryNotFoundError()
    author_id = getattr(history, 'author_id', None) 
    if author_id is None:
        app_logger.error(f"Пользователь {author_id} не найден")
        raise UserNotFoundError()
    if author_id != user.id:
        app_logger.warning(f"Пользователь {user.id} попытался получить доступ к истории {id}")
        raise OwnershipHistoryError()
    return history


async def get_like_or_error(id: int, user: User) -> HistoryLike:
    """
    Получает лайк из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    like = await like_manager.get_obj_by_id(id=id)
    if not like:
        app_logger.error(f"Лайк {id} не найден")
        raise LikeNotFoundError()
    user_id = getattr(like, 'user_id', None)
    if user_id is None:
        app_logger.error(f"Пользователь {user_id} не найден")
        raise UserNotFoundError()
    if user_id != user.id:
        app_logger.warning(f"Пользователь {user.id} попытался получить доступ к лайку {id}")
        raise OwnershipLikeError()
    return like
