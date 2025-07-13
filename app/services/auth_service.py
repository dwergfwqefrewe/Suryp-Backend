from database.managers.user_manager import UserManager
from schemas.user import UserAuth, UserCreate

from core.jwt import create_access_token, create_refresh_token
from core.logger import app_logger

from exceptions.users import InvalidCredentialsError


user_manager = UserManager()

async def register_user(new_user: UserCreate) -> tuple[str, str]:
    """
    Регистрирует нового пользователя и выдает токены
    """
    created_user = await user_manager.create_user(new_user)
    access_token = create_access_token({"sub": str(created_user.id)})
    refresh_token = create_refresh_token({"sub": str(created_user.id)})
    app_logger.info(f"Пользователь {new_user.login} зарегистрирован")
    return access_token, refresh_token

async def login_user(user: UserAuth) -> tuple[str, str]:
    """
    Авторизует пользователя и выдает токены
    """
    user = await user_manager.check_user_data(user)
    if not user:
        raise InvalidCredentialsError()
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    app_logger.info(f"Пользователь {user.login} авторизован")
    return access_token, refresh_token
