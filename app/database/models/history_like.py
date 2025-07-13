from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.config import Base


class HistoryLike(Base):
    """Модель для связи истории и пользователя
        - id - id лайка
        - created_at - дата и время постановки лайка
        - user_id - id пользователя, который поставил лайк
        - history_id - id истории, которой поставили лайк
        - user - пользователь, который поставил лайк
        - history - история, которой поставили лайк
    """
    __tablename__ = 'history_likes' 

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer,
                          ForeignKey('users.id',
                                     ondelete='CASCADE'),
                                     nullable=False)
    
    history_id = Column(Integer,
                             ForeignKey('histories.id',
                                        ondelete='CASCADE'),
                                        nullable=False)
    
    user = relationship('User', back_populates='history_likes')
    history = relationship('History', back_populates='history_likes')

    __table_args__ = (
        # Уникальность для связи пользователя и истории
        UniqueConstraint('user_id',
                         'history_id',
                         name='uix_user_history_like'),
    )
