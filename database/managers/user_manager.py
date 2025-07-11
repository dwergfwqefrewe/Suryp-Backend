import bcrypt
from typing import Optional

from .base_manager import BaseManager
from .session_manager import manager
from models.user import User
from schemas.user import UpdateUser, UserAuth, UserCreate
from exceptions import DatabaseError
from sqlalchemy.future import select

class UserManager(BaseManager[User, UpdateUser]):
    """
    Менеджер для работы с пользователями (асинхронный)
    """
    def __init__(self) -> None:
        super().__init__(User)

    async def get_user_by_login(self, login: str) -> Optional[User]:
        async with manager.get_async_session() as session:
            result = await session.execute(select(User).where(User.login == login))
            return result.scalars().first()

    async def get_user_id_by_login(self, login: str) -> Optional[int]:
        user = await self.get_user_by_login(login)
        return getattr(user, "id", None) if user else None

    async def create_user(self, user_create: UserCreate) -> User:
        """
        Создание пользователя с хешированием пароля (асинхронно)
        """
        try:
            password = user_create.password
            obj_dict = user_create.model_dump(exclude={"password"})
            user = User(**obj_dict)
            setattr(user, "password_hash", self._hash_password(password))
            async with manager.get_async_session() as session:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
        except Exception as e:
            raise DatabaseError(f"Ошибка при создании пользователя: {str(e)}")

    async def create_obj(self, obj: User) -> User:
        """
        Создание пользователя, если уже User (асинхронно)
        """
        try:
            if getattr(obj, "password_hash", None) in (None, ""):
                raise ValueError("User model must have 'password_hash' set")
            async with manager.get_async_session() as session:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
        except Exception as e:
            raise DatabaseError(f"Ошибка при создании пользователя: {str(e)}")

    async def check_user_data(self, user: UserAuth) -> Optional[User]:
        """
        Проверка данных пользователя (асинхронно)
        """
        db_user = await self.get_user_by_login(user.login)
        if not db_user:
            return None
        db_password_hash = getattr(db_user, "password_hash", None)
        if db_password_hash and bcrypt.checkpw(user.password.encode("utf-8"), db_password_hash.encode("utf-8")):
            return db_user
        return None

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
