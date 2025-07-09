import bcrypt

from .base_manager import BaseManager
from .session_manager import manager
from models.user import User
from schemas.user import UpdateUser, UserAuth, UserCreate


class UserManager(BaseManager[User, UpdateUser]):
    """Менеджер для работы с пользователями"""

    def __init__(self) -> None:
        super().__init__(User)

    @staticmethod
    def get_user_id_by_login(login: str) -> int | None:
        """Получение id пользователя по логину
            - login - логин пользователя
        """
        with manager.get_session() as session:
            user = session.query(User).filter(User.login == login).first()
            return user.id if user else None

    def create_obj(self, obj: User | UserCreate) -> User:
        """Создание пользователя с хешированием пароля"""
        if isinstance(obj, UserCreate):
            password = obj.password
            obj_dict = obj.model_dump(exclude={"password"})
            obj = User(**obj_dict)
            obj.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        elif isinstance(obj, User):
            # Если передали User с password_hash, ничего не делаем
            if not obj.password_hash:
                raise ValueError("User model must have 'password_hash' set")

        else:
            raise ValueError("Invalid object type passed to create_obj")

        with manager.get_session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    @staticmethod
    def check_user_data(user: UserAuth) -> User | None:
        """Проверка данных пользователя
            - user - данные пользователя
        """
        with manager.get_session() as session:
            db_user = session.query(User).filter(User.login == user.login).first()
            if not db_user:
                return None
            if bcrypt.checkpw(user.password.encode("utf-8"),
                              db_user.password_hash.encode("utf-8")):
                return db_user
            return None
