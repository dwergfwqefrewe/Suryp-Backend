from fastapi import HTTPException, Request
from jose import JWTError

from api.auth_config import JWT_ACCESS_COOKIE_NAME, JWT_REFRESH_COOKIE_NAME

from models.user import User
from models.history import History as _History
from models.comments import Comment as _Comment
from models.history_like import HistoryLike as _Like

from database.managers.history_manager import HistoryManager
from database.managers.comment_manager import CommentManager
from database.managers.like_manager import LikeManager
from database.managers.user_manager import UserManager

from .jwt_auth import decode_token


user_manager = UserManager()
history_manager = HistoryManager()
comment_manager = CommentManager()
like_manager = LikeManager()


async def get_current_user(request: Request) -> User:
    """
    Получает пользователя из БД по access token из cookies
    """
    token = request.cookies.get(JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Отсутствует access токен")
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Неверный токен")
    user = await user_manager.get_obj_by_id(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


async def validate_refresh_token(request: Request) -> int:
    """
    Проверяет refresh токен и возвращает ID пользователя
    """
    token = request.cookies.get(JWT_REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(401, detail="Отсутствует refresh токен")

    try:
        user_id = int(decode_token(token).get("sub") or 0)
    except (JWTError, ValueError):
        raise HTTPException(401, detail="Неверный токен")

    user = await user_manager.get_obj_by_id(user_id)
    if not user:
        raise HTTPException(401, detail="Пользователь не найден")

    return user_id  


async def get_comment_or_error(id: int, user: User) -> _Comment:
    """
    Получает комментарий из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    comment = await comment_manager.get_obj_by_id(id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    user_id = getattr(comment, 'user_id', None)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к комментарию")
    return comment


async def get_history_or_error(id: int, user: User) -> _History:
    """
    Получает историю из БД по ID и проверяет, что она принадлежит текущему пользователю
    """
    history = await history_manager.get_obj_by_id(id=id)
    if not history:
        raise HTTPException(status_code=404, detail="История не найдена")
    author_id = getattr(history, 'author_id', None) 
    if author_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if author_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к истории")
    return history


async def get_like_or_error(id: int, user: User) -> _Like:
    """
    Получает лайк из БД по ID и проверяет, что он принадлежит текущему пользователю
    """
    like = await like_manager.get_obj_by_id(id=id)
    if not like:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    user_id = getattr(like, 'user_id', None)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к лайку")
    return like
