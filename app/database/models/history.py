from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.config import Base


class History(Base):
    """Модель для истории
        - id - id истории
        - title - заголовок истории
        - description - описание истории
        - likes - количество лайков
        - created_at - дата и время создания истории
        - updated_at - дата и время обновления истории
        - author_id - id автора истории
        - author - автор истории
        - history_likes - связь с лайками истории
        - comments_rel - связь с комментариями истории
    """
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String(1000))
    likes = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    
    updated_at = Column(DateTime,
                            default=None,
                            onupdate=datetime.utcnow)

    author_id = Column(Integer,
                            ForeignKey('users.id'),
                            nullable=False)

    author = relationship('User', back_populates='histories')

    history_likes = relationship('HistoryLike',
                                 back_populates='history',
                                 cascade='all, delete')

    comments_rel = relationship('Comment',
                                 back_populates='history',
                                 cascade='all, delete')
