from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):   
    """Схема для создания комментария"""
    content: str
    article_id: int
    user_id: int


class CommentCreate(CommentBase):
    """Схема для создания комментария"""
    pass


class CommentUpdate(BaseModel):
    """Схема для обновления комментария"""
    content: str | None


class CommentOut(BaseModel):
    """Схема для получения комментария"""
    id: int
    user_id: int
    article_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
