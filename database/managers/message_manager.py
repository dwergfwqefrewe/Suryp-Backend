from typing import List
from sqlalchemy import or_, and_
from models.message import Message
from database.managers.base_manager import BaseManager
from database.managers.session_manager import manager


class MessageManager(BaseManager[Message, None]):
    def __init__(self):
        super().__init__(Message)


    def save_message(self, sender_id: int, receiver_id: int, text: str) -> Message:
        with manager.get_session() as session:
            message = Message(sender_id=sender_id,
                              receiver_id=receiver_id,
                              text=text)
            session.add(message)
            session.commit()
            session.refresh(message)
            return message


    def get_history(self, user1_id: int, user2_id: int) -> List[Message]:
        with manager.get_session() as session:
            return session.query(Message).filter(
                or_(
                    and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                    and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
                )
            ).order_by(Message.timestamp.asc()).all()


    def get_chats(self, user_id: int) -> List[Message]:
        with manager.get_session() as session:
            return session.query(Message).filter(
                or_(
                    Message.sender_id == user_id,
                    Message.receiver_id == user_id
                )
            ).order_by(Message.timestamp.desc()).all()
