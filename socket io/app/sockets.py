import socketio
import logging
from typing import Dict, Any
from database.managers.message_manager import MessageManager
from models.user import User
from schemas.message import MessageSchema
from database.managers.user_manager import UserManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Socket.IO сервер
sio = socketio.AsyncServer(
    async_mode='asgi', 
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)

user_manager = UserManager()

def socket_app(app):
    """Создает ASGI приложение с Socket.IO"""
    return socketio.ASGIApp(sio, other_asgi_app=app)

# Хранилище подключенных пользователей
users: Dict[str, str] = {}

message_manager = MessageManager()

@sio.event
async def connect(sid: str, environ: Dict[str, Any]) -> None:
    """Обработчик подключения пользователя"""
    logger.info(f'Пользователь подключился: {sid}')
    await sio.emit('user_count', {'count': len(users) + 1}, skip_sid=sid)
    username = users.get(sid)
    if username:
        user_id = user_manager.get_user_id_by_login(username)
        if user_id:
            history = message_manager.get_history(user_id, user_id)
            history_data = [MessageSchema.model_validate(m).model_dump() for m in history]
            await sio.emit('history', history_data, to=sid)


@sio.event
async def disconnect(sid: str) -> None:
    """Обработчик отключения пользователя"""
    username = users.pop(sid, "Аноним")
    await sio.emit('message', {
        "user": "Система", 
        "text": f"{username} покинул чат.",
        "type": "system"
    })
    await sio.emit('user_count', {'count': len(users)})
    logger.info(f'Пользователь отключился: {sid} ({username})')


@sio.event
async def join(sid: str, data: Dict[str, Any]) -> None:
    """Обработчик присоединения к чату"""
    username = data.get("username", "Аноним")
    users[sid] = username
    
    await sio.emit('message', {
        "user": "Система", 
        "text": f"{username} присоединился к чату.",
        "type": "system"
    })
    await sio.emit('user_count', {'count': len(users)})
    
    logger.info(f"{username} присоединился ({sid})")


@sio.event
async def message(sid: str, data: Dict[str, Any]) -> None:
    """Обработчик сообщений"""
    username = users.get(sid, "Аноним")
    text = data.get("text", "").strip()
    receiver_username = data.get("receiver")  # предполагается, что клиент передает получателя
    if not text:
        return
    
    user_manager = UserManager()
    sender_id = user_manager.get_user_id_by_login(username)
    receiver_id = user_manager.get_user_id_by_login(receiver_username) if receiver_username else None
    if sender_id and receiver_id:
        message_manager.save_message(sender_id, receiver_id, text)
    await sio.emit('message', {
        "user": username, 
        "text": text,
        "type": "user"
    })
    logger.info(f"Сообщение от {username}: {text}")


@sio.event
async def typing(sid: str, data: Dict[str, Any]) -> None:
    """Обработчик индикатора печати"""
    username = users.get(sid, "Аноним")
    is_typing = data.get("is_typing", False)
    
    await sio.emit('typing', {
        "user": username,
        "is_typing": is_typing
    }, skip_sid=sid) 


@sio.event
async def get_history(sid: str, data: Dict[str, Any]) -> None:
    """Получение истории сообщений между двумя пользователями"""
    username = data.get("username")
    companion = data.get("companion")
    if not username or not companion:
        await sio.emit('history', [], to=sid)
        return
    user_id = user_manager.get_user_id_by_login(username)
    companion_id = user_manager.get_user_id_by_login(companion)
    if user_id and companion_id:
        history = message_manager.get_history(user_id, companion_id)
        history_data = [MessageSchema.model_validate(m).model_dump() for m in history]
        await sio.emit('history', history_data, to=sid)
    else:
        await sio.emit('history', [], to=sid) 
