from pydantic import BaseModel
from datetime import datetime

from schemas.author import AuthorOut


class HistoryCreate(BaseModel):
    """Схема для создания статьи"""
    title: str
    description: str | None = None  


class HistoryOut(BaseModel):
    """Схема для получения статьи"""
    id: int
    title: str
    description: str | None = None
    likes: int
    author: AuthorOut | None
    created_at: datetime
    updated_at: datetime | None = None  

    class Config:
        from_attributes = True


class HistoryOutShort(BaseModel):
    id: int
    title: str
    description: str | None = None
    likes: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class HistoryUpdate(BaseModel):
    """Схема для обновления статьи"""
    title: str | None = None
    description: str | None = None
