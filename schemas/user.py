from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая схема для пользователя:
        - login (str) - логин пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
    """
    login: str
    about: str | None = None
    avatar_url: str | None = None


class UserCreate(UserBase):
    """Схема для создания пользователя:
        - login (str) - логин пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
        - password (str) - пароль пользователя
    """
    password: str


class UserOut(UserBase):
    """Схема для получения пользователя:
        - id (int) - id пользователя
        - role (int) - роль пользователя
        - histories (List[HistoryOut]) - список историй пользователя
    """
    id: int
    role: int


class UserAuth(BaseModel):
    """Схема для входа в систему:
        - login (str) - логин пользователя
        - password (str) - пароль пользователя
    """
    login: str
    password: str


class UpdateUser(BaseModel):
    """Схема для обновления пользователя:
        - login (str | None) - логин пользователя
        - password (str | None) - пароль пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
    """
    login: str | None = None
    password: str | None = None
    about: str | None = None
    avatar_url: str | None = None


class UpdateMe(BaseModel):
    """Схема для частичного обновления данных о себе:
        - about (str | None)
        - avatar_url (str | None)
    """
    about: str | None = None
    avatar_url: str | None = None
