from .base_manager import BaseManager
from .session_manager import manager
from models.user import User
from schemas.user import UpdateUser, UserAuth


class UserManager(BaseManager[User, UpdateUser]):
    """Менеджер для работы с пользователями"""

    def __init__(self) -> None:
        super().__init__(User)


    def get_user_id_by_login(self, login: str) -> int | None:
        """Получение id пользователя по логину
            - login - логин пользователя
        """
        with manager.get_session() as session:
            user = session.query(User).filter(User.login == login).first()
            return user.id if user else None
        

    def check_user_data(self, user: UserAuth) -> User | None:
        """Проверка данных пользователя
            - user - данные пользователя
        """
        with manager.get_session() as session:
            return session.query(User).filter(User.login == user.login,
                                              User.password_hash == user.password_hash)\
                                              .first()
        