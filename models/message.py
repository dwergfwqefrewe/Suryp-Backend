from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.config import Base

class Message(Base):
    """Модель для хранения сообщений
        - id: первичный ключ
        - sender_id: id отправителя (user)
        - receiver_id: id получателя (user)
        - text: текст сообщения
        - timestamp: время отправки
    """
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    sender = relationship('User',
                            foreign_keys=[sender_id],
                            backref='sent_messages')
                            
    receiver = relationship('User',
                            foreign_keys=[receiver_id],
                            backref='received_messages')
