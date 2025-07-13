import datetime
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status
)

from database.managers.message_manager import MessageManager
from database.managers.user_manager import UserManager
from database.models.user import User
from schemas.chat import ChatOut

from api.dependencies.auth import get_current_user

from core.logger import app_logger

from exceptions.base import DatabaseError
from exceptions.message import MessageNotFoundError, OwnershipMessageError
from exceptions.users import UserNotFoundError

from api.docs.message import get_chats_responses

message_router = APIRouter(prefix="/messages", tags=["Сообщения"])

message_manager = MessageManager()
user_manager = UserManager()


@message_router.get("/chats",
                    summary="Получить все чаты",
                    status_code=status.HTTP_200_OK,
                    responses=get_chats_responses)
async def get_chats(user: User = Depends(get_current_user)) -> List[ChatOut]:
    try:
        user_id = getattr(user, 'id', 0)
        if not user:
            raise UserNotFoundError()
        chats = await message_manager.get_chats(getattr(user, 'id', 0))
        app_logger.info(f"Получены чаты для пользователя {user.login}")
        companion_ids = []
        for chat in chats:
            if bool(chat.sender_id == user_id):
                companion_ids.append(chat.receiver_id)
            else:
                companion_ids.append(chat.sender_id)
        companion_ids = list(set(companion_ids))
        companions = [await user_manager.get_obj_by_id(uid) for uid in companion_ids]
        app_logger.info(f"Получены собеседники для пользователя {user.login}")
        chats_out = []
        for comp in companions:
            last_msg = await message_manager.get_last_message(str(user.login), str(comp.login))
            chats_out.append(ChatOut(
                companion_login=str(comp.login),
                companion_avatar_url=str(comp.avatar_url) if comp.avatar_url is not None else None,
                last_message=str(getattr(last_msg, 'text', None)),
                last_message_time=getattr(last_msg, 'timestamp', datetime.datetime.now()),
                from_me=bool(getattr(last_msg, 'sender_id', 0) == user_id)
            ))
        app_logger.info(f"Получены последние сообщения для пользователя {user.login}")
        return chats_out
    except (MessageNotFoundError, OwnershipMessageError, UserNotFoundError) as e:
        raise e
    except Exception as e:
        app_logger.error(f"Ошибка при получении чатов: {e}")
        raise DatabaseError("Ошибка при получении чатов")
