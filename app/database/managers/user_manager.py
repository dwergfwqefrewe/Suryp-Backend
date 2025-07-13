from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

import bcrypt

from database.managers.session_manager import manager
from database.managers.base_manager import BaseManager

from database.models.user import User
from schemas.user import UpdateUser, UserAuth, UserCreate

from exceptions.users import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)
from exceptions.base import DatabaseError


from core.logger import app_logger

class UserManager(BaseManager[User, UpdateUser]):
    """
    Менеджер для работы с пользователями (асинхронный)
    """
    def __init__(self) -> None:
        super().__init__(User)

    async def get_user_by_login(self, login: str) -> User:
        """Получение пользователя по логину"""
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(select(User).where(User.login == login))
                user = result.scalars().first()
                if not user:
                    raise UserNotFoundError()
                return user
        except Exception as e:
            app_logger.exception(f"Неизвестная ошибка при получении пользователя по логину {login} Traceback: {e.__traceback__}")
            raise DatabaseError()

    async def get_user_id_by_login(self, login: str) -> int:
        """Получение id пользователя по логину"""
        try:
            user = await self.get_user_by_login(login)
            if not user:
                raise UserNotFoundError()
            return getattr(user, "id", 0)
        except Exception as e:
            app_logger.exception(f"Неизвестная ошибка при получении id пользователя по логину {login} Traceback: {e.__traceback__}")
            raise DatabaseError()

    async def create_user(self, user_create: UserCreate) -> User:
        """Создание пользователя, если пользователь с таким логином уже существует, то выбрасывается исключение"""
        password = user_create.password
        obj_dict = user_create.model_dump(exclude={"password"})
        user = User(**obj_dict)
        setattr(user, "password_hash", self._hash_password(password))
        async with manager.get_async_session() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as e:
                await session.rollback()
                app_logger.exception(f"Попытка создания пользователя с логином {user_create.login}, который уже существует")
                raise UserAlreadyExistsError()
            except Exception as e:
                await session.rollback()
                app_logger.exception(f"Неизвестная ошибка при создании пользователя Traceback: {e.__traceback__}")
                raise DatabaseError()

    async def check_user_data(self, user: UserAuth) -> User:
        """Проверка данных пользователя"""
        try:
            db_user = await self.get_user_by_login(user.login)
            if not db_user:
                app_logger.warning(f"Пользователь {user.login} не найден")
                raise UserNotFoundError()
            db_password_hash = getattr(db_user, "password_hash", None)
            if db_password_hash and bcrypt.checkpw(user.password.encode("utf-8"), db_password_hash.encode("utf-8")):
                return db_user
            raise InvalidCredentialsError()
        except Exception as e:
            app_logger.exception(f"Неизвестная ошибка при проверке данных пользователя {user.login} Traceback: {e}")
            raise DatabaseError()

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
