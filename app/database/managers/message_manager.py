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

    async def save_message(self, sender_id: int, receiver_id: int, text: str) -> Message:
        try:
            async with manager.get_async_session() as session:
                message = Message(sender_id=sender_id, receiver_id=receiver_id, text=text)
                session.add(message)
                await session.commit()
                await session.refresh(message)
                return message
        except Exception as e:
            app_logger.exception(f"Ошибка при сохранении сообщения sender_id={sender_id}, receiver_id={receiver_id}")
            raise DatabaseError(f"Ошибка при сохранении сообщения sender_id={sender_id}, receiver_id={receiver_id}")

    async def get_history(self, user1_id: int, user2_id: int) -> List[Message]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message).where(self._chat_filter(user1_id, user2_id)).order_by(Message.timestamp.asc())
                )
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Ошибка при получении истории сообщений user1_id={user1_id}, user2_id={user2_id}")
            raise DatabaseError(f"Ошибка при получении истории сообщений user1_id={user1_id}, user2_id={user2_id}")

    async def get_chats(self, user_id: int) -> List[Message]:
        try:
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message).where(
                        or_(
                            Message.sender_id == user_id,
                            Message.receiver_id == user_id
                        )
                    ).order_by(Message.timestamp.desc())
                )
                return list(result.scalars().all())
        except Exception as e:
            app_logger.exception(f"Ошибка при получении чатов user_id={user_id}")
            raise DatabaseError(f"Ошибка при получении чатов user_id={user_id}")

    async def get_last_message(self, first_login: str, second_login: str) -> Optional[Message]:
        try:
            first_id = await user_manager.get_user_id_by_login(first_login)
            second_id = await user_manager.get_user_id_by_login(second_login)
            if first_id is None or second_id is None:
                return None
            async with manager.get_async_session() as session:
                result = await session.execute(
                    select(Message).where(self._chat_filter(first_id, second_id)).order_by(Message.timestamp.desc())
                )
                return result.scalars().first()
        except Exception as e:
            app_logger.exception(f"Ошибка при получении последнего сообщения first_login={first_login}, second_login={second_login}")
            raise DatabaseError(f"Ошибка при получении последнего сообщения first_login={first_login}, second_login={second_login}")
