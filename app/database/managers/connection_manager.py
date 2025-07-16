from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, room_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[room_id][user_id] = websocket

    async def disconnect(self, user_id: str, room_id: str):
        self.active_connections[room_id].pop(user_id)

    async def send_to_room(self, room_id: str, message: str):
        for connection in self.active_connections[room_id].values():
            await connection.send_text(message)
