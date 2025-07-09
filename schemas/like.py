from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    """Схема для создания лайка:
        - article_id - id статьи, которой поставили лайк
        - user_id - id пользователя, который поставил лайк
    """
    article_id: int
    user_id: int


class LikeCreate(LikeBase):
    pass


class LikeUpdate(BaseModel):
    pass


class LikeOut(BaseModel):
    """Схема для получения информации о лайке:
        - id - id лайка
        - user_id - id пользователя, который поставил лайк
        - article_id - id статьи, которой поставили лайк
        - created_at - дата и время постановки лайка
    """
    id: int
    user_id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True
