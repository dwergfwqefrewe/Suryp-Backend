from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status
)

from database.managers.message_manager import MessageManager
from database.managers.user_manager import UserManager

from models.user import User
from schemas.chat import ChatOut
from schemas.user import UserBase

from .dependencies import get_current_user

message_router = APIRouter(prefix="/messages", tags=["Сообщения"])

message_manager = MessageManager()
user_manager = UserManager()


@message_router.get("/chats",
                    summary="Получить все чаты",
                    status_code=status.HTTP_200_OK)
def get_chats(user: User = Depends(get_current_user)) -> List[ChatOut]:
    chats = message_manager.get_chats(user.id)

    companion_ids = {
        chat.receiver_id if chat.sender_id == user.id else chat.sender_id
        for chat in chats
    }

    companions = [user_manager.get_obj_by_id(uid) for uid in companion_ids]

    chats = []
    for comp in companions:
        last_msg = message_manager.get_last_message(user.login, comp.login)
        chats.append(ChatOut(
            companion_login=comp.login,
            companion_avatar_url=comp.avatar_url,
            last_message=last_msg.text,
            last_message_time=last_msg.timestamp,
            from_me=last_msg.sender_id == user.id
        ))
    return chats
