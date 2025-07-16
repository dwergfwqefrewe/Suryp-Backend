from typing import List, Optional

from sqlalchemy import or_, and_
from sqlalchemy.future import select

from database.managers.user_manager import UserManager
from database.managers.base_manager import BaseManager
from database.managers.session_manager import manager

from database.models.message import Message
from schemas.message import MessageUpdate

from exceptions.base import DatabaseError

from core.logger import app_logger


user_manager = UserManager()

class MessageManager(BaseManager[Message, MessageUpdate]):
    def __init__(self):
        super().__init__(Message)

    def _chat_filter(self, user1_id: int, user2_id: int):
        return or_(
            and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
            and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
        )

    async def save_message(self, sender_id: int, receiver_id: int, text: str, room_id: str) -> Message:
        try:
            async with manager.get_async_session() as session:
                message = Message(sender_id=sender_id, receiver_id=receiver_id, text=text, room_id=room_id)
                session.add(message)
                await session.commit()
                await session.refresh(message)
                return message
        except Exception as e:
            app_logger.exception(f"Ошибка при сохранении сообщения sender_id={sender_id}, receiver_id={receiver_id}")
            raise DatabaseError(f"Ошибка при сохранении сообщения sender_id={sender_id}, receiver_id={receiver_id}")

    async def get_history(self, room_id: str) -> List[Message]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message).where(Message.room_id == room_id).order_by(Message.timestamp.asc())
                )
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Ошибка при получении истории сообщений room_id={room_id}")
            raise DatabaseError(f"Ошибка при получении истории сообщений room_id={room_id}")

    async def get_room_ids_by_user_id(self, user_id: int) -> List[str]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message.room_id).where(Message.sender_id == user_id).distinct(Message.room_id)  
                )
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Ошибка при получении чатов user_id={user_id}")
            raise DatabaseError(f"Ошибка при получении чатов user_id={user_id}")

    async def get_last_message_by_room_id(self, room_id: str) -> Optional[Message]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message).where(Message.room_id == room_id).order_by(Message.timestamp.desc())
                )
                return result.scalars().first()
        except Exception as e:
            app_logger.exception(f"Ошибка при получении последнего сообщения room_id={room_id}")
            raise DatabaseError(f"Ошибка при получении последнего сообщения room_id={room_id}")

    async def get_history(self, room_id: str) -> List[Message]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(select(Message).where(Message.room_id == room_id))
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Ошибка при получении истории сообщений room_id={room_id}")
            raise DatabaseError(f"Ошибка при получении истории сообщений room_id={room_id}")
