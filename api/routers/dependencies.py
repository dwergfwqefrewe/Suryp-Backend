from fastapi import HTTPException, Request
from jose import JWTError
from sqlalchemy.orm import selectinload

from .jwt_auth import decode_token
from api.auth_config import JWT_ACCESS_COOKIE_NAME
from database.managers.user_manager import UserManager
from models.user import User
from models.history import History as _History
from models.comments import Comment as _Comment
from models.history_like import HistoryLike as _Like
from database.managers.history_manager import HistoryManager
from database.managers.comment_manager import CommentManager
from database.managers.like_manager import LikeManager


user_manager = UserManager()
history_manager = HistoryManager()
comment_manager = CommentManager()
like_manager = LikeManager()


def get_current_user(request: Request) -> User:
    """
    Получает пользователя из БД по access token из cookies
    """
    token = request.cookies.get(JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid Token")
    user = user_manager.get_obj_by_id(
        id=user_id,
        options=[selectinload(User.histories).selectinload(_History.author)]
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_comment_or_error(id: int, user: User) -> _Comment:
    """
    Получает комментарий из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    comment = comment_manager.get_obj_by_id(id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к комментарию")
    return comment


def get_history_or_error(id: int, user: User) -> _History:
    """
    Получает историю из БД по ID и проверяет, что она принадлежит текущему пользователю
    """
    history = history_manager.get_history_by_id_with_author(id=id)
    if not history:
        raise HTTPException(status_code=404, detail="История не найдена")
    if history.author_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к истории")
    return history


def get_like_or_error(id: int, user: User) -> _Like:
    """
    Получает лайк из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    like = like_manager.get_obj_by_id(id=id)
    if not like:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    if like.user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к лайку")
    return like
