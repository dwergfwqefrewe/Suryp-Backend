from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    """Схема для создания лайка:
        - history_id - id статьи, которой поставили лайк
    """
    history_id: int 


class LikeCreate(LikeBase):
    pass


class LikeUpdate(BaseModel):
    pass


class LikeOut(BaseModel):
    """Схема для получения информации о лайке:
        - id - id лайка
        - user_id - id пользователя, который поставил лайк
        - history_id - id статьи, которой поставили лайк
        - created_at - дата и время постановки лайка
    """
    id: int
    user_id: int
    history_id: int
    created_at: datetime 

    class Config:
        from_attributes = True
