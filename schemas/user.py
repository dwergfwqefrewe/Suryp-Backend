from typing import List

from pydantic import BaseModel, computed_field

from schemas.article import ArticleOut


class UserBase(BaseModel):
    """Базовая схема для пользователя:
        - login (str) - логин пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
    """
    login: str
    about: str | None
    avatar_url: str | None


class UserCreate(UserBase):
    """Схема для создания пользователя:
        - login (str) - логин пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
        - password_hash (str) - хэш пароля пользователя
    """
    password_hash: str


class UserOut(UserBase):
    """Схема для получения пользователя:
        - id (int) - id пользователя
        - role (int) - роль пользователя
        - articles (List[ArticleOut]) - список статей пользователя
    """
    id: int
    role: int
    articles: List[ArticleOut]

    @computed_field
    @property
    def articles_count(self) -> int:
        """Метод для получения количества статей пользователя"""
        return len(self.articles)
    
    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    """Схема для входа в систему:
        - login (str) - логин пользователя
        - password_hash (str) - хэш пароля пользователя
    """
    login: str
    password_hash: str


class UpdateUser(BaseModel):
    """Схема для обновления пользователя:
        - login (str | None) - логин пользователя
        - password_hash (str | None) - хэш пароля пользователя
        - about (str | None) - описание пользователя
        - avatar_url (str | None) - url аватара пользователя
    """
    login: str | None = None
    password_hash: str | None = None
    about: str | None = None
    avatar_url: str | None = None


class UpdateMe(BaseModel):
    """Схема для частичного обновления данных о себе:
        - about (str | None)
        - avatar_url (str | None)
    """
    about: str | None = None
    avatar_url: str | None = None
