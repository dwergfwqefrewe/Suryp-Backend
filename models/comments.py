from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database.config import Base


class Comment(Base):
    """Модель для комментария
        - id - id комментария
        - content - текст комментария
        - created_at - дата и время создания комментария
        - updated_at - дата и время последнего обновления комментария
        - user_id - id пользователя, который оставил комментарий
        - history_id - id истории, к которой оставили комментарий
        - user - пользователь, который оставил комментарий
        - history - история, к которой оставили комментарий
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


    user_id = Column(Integer,
                          ForeignKey('users.id',
                                     ondelete='CASCADE'),
                          nullable=False) 
    
    history_id = Column(Integer,
                             ForeignKey('histories.id',
                                        ondelete='CASCADE'),
                             nullable=False)
    
    user = relationship('User', back_populates='comments')
    history = relationship('History', back_populates='comments_rel')
