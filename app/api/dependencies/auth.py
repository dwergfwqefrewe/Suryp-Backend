from fastapi import Request, HTTPException
from jose import JWTError

from database.models.user import User

from api.auth_config import JWT_ACCESS_COOKIE_NAME, JWT_REFRESH_COOKIE_NAME
from exceptions.users import UserNotFoundError
from exceptions.base import PermissionError, ValidationError
from core.jwt import decode_token
from database.managers.user_manager import UserManager

from core.logger import app_logger  

user_manager = UserManager()

async def get_current_user(request: Request) -> User:
    """
    Получает пользователя из БД по access token из cookies
    """
    token = request.cookies.get(JWT_ACCESS_COOKIE_NAME)
    if not token:
        app_logger.error("Отсутствует access токен")
        raise PermissionError("Отсутствует access токен")
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            app_logger.error(f"Неверный токен sub: {sub} token: {token}")
            raise ValidationError("Неверный токен")
        user_id = int(sub)
    except (JWTError, ValueError):
        app_logger.error(f"Неверный токен: {token}")
        raise ValidationError("Неверный токен")
    try:
        user = await user_manager.get_obj_by_id(id=user_id)
    except UserNotFoundError as e:
        app_logger.error(f"Пользователь {user_id} не найден")
        raise UserNotFoundError()
    return user


async def validate_refresh_token(request: Request) -> int:
    """
    Проверяет refresh токен и возвращает ID пользователя
    """
    refresh_token = request.cookies.get(JWT_REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise PermissionError("Отсутствует refresh токен")
    try:
        payload = decode_token(refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise ValidationError(f"Неверный токен sub: {sub} refresh_token: {refresh_token}")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise ValidationError(f"Неверный токен refresh_token: {refresh_token}")

    try:
        user = await user_manager.get_obj_by_id(user_id)
    except UserNotFoundError:
        raise UserNotFoundError()

    return user_id
