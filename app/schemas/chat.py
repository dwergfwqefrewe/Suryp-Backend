from pydantic import BaseModel
from datetime import datetime

class ChatOut(BaseModel):
    companion_login: str
    companion_avatar_url: str | None
    last_message: str
    last_message_time: datetime
    room_id: str
    from_me: bool
    #is_read: bool

    class Config:
        from_attributes = True
