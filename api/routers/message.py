from fastapi import (
    APIRouter,
    Depends,
    status
)
from typing import List
from models.user import User
from schemas.user import UserBase
from database.managers.message_manager import MessageManager
from database.managers.user_manager import UserManager
from .dependencies import get_current_user

message_router = APIRouter(prefix="/messages", tags=["Сообщения"])

message_manager = MessageManager()
user_manager = UserManager()


@message_router.get("/chats",
                    summary="Получить все чаты",
                    status_code=status.HTTP_200_OK)
def get_chats(user: User = Depends(get_current_user)) -> List[UserBase]:
    chats = message_manager.get_chats(user.id)

    companion_ids = {
        chat.receiver_id if chat.sender_id == user.id else chat.sender_id
        for chat in chats
    }

    companions = [user_manager.get_obj_by_id(uid) for uid in companion_ids]

    return [
        UserBase(
            id=comp.id,
            login=comp.login,
            about=comp.about,
            avatar_url=comp.avatar_url
        )
        for comp in companions if comp
    ]
