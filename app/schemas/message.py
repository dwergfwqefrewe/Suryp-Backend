from pydantic import BaseModel
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int 
    text: str
    timestamp: datetime
    from_me: bool

    class Config:
        from_attributes = True


class MessageUpdate(BaseModel):
    text: str

    class Config:
        from_attributes = True
        