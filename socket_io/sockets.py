import logging
from typing import Dict, Any

import socketio

from api.routers.jwt_auth import decode_token
from database.managers.message_manager import MessageManager

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)

def socket_app(app):
    return socketio.ASGIApp(sio, other_asgi_app=app)


connected_users: Dict[str, int] = {}

message_manager = MessageManager()


@sio.event
async def connect(sid: str, environ: Dict[str, Any]) -> None:
    logger.info(f"[connect] {sid} подключился")


@sio.event
async def disconnect(sid: str) -> None:
    user_id = connected_users.pop(sid, None)
    if user_id:
        room = f"user_{user_id}"
        await sio.leave_room(sid, room)
        logger.info(f"[disconnect] {user_id} вышел из комнаты {room}")
    else:
        logger.info(f"[disconnect] {sid} отключился без user_id")


@sio.event
async def join(sid: str, data: Dict[str, Any]) -> None:
    token = data.get("token")
    if not token:
        logger.warning(f"[join] Нет токена от {sid}")
        return

    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except Exception as e:
        logger.warning(f"[join] Невалидный токен от {sid}: {e}")
        return

    connected_users[sid] = user_id
    room = f"user_{user_id}"
    await sio.enter_room(sid, room)
    logger.info(f"[join] Пользователь {user_id} вошёл в комнату {room}")


@sio.event
async def message(sid: str, data: Dict[str, Any]) -> None:
    sender_id = connected_users.get(sid)
    if not sender_id:
        logger.warning(f"[message] {sid} не аутентифицирован")
        return

    receiver_id = data.get("receiver_id")
    text = data.get("text", "").strip()
    if not text or not receiver_id:
        logger.warning(f"[message] Неверные данные от {sender_id}")
        return

    message = message_manager.save_message(sender_id, receiver_id, text)

    msg_payload = {
        "id": message.id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "text": message.text,
        "timestamp": message.timestamp.isoformat()
    }

    # Отправляем обоим участникам
    await sio.emit("message", msg_payload, room=f"user_{receiver_id}")
    await sio.emit("message", msg_payload, room=f"user_{sender_id}")
    logger.info(f"[message] {sender_id} -> {receiver_id}: {text}")


@sio.event
async def typing(sid: str, data: Dict[str, Any]) -> None:
    sender_id = connected_users.get(sid)
    receiver_id = data.get("receiver_id")
    is_typing = data.get("is_typing", False)

    if not sender_id or not receiver_id:
        return

    await sio.emit("typing", {
        "sender_id": sender_id,
        "is_typing": is_typing
    }, room=f"user_{receiver_id}")
