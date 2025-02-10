from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Message(BaseModel):
    role: str  # 'user' or 'ai'
    content: str
    timestamp: str = None

class ChatRoom(BaseModel):
    chat_room_id: str
    message_id: int
    messages: List[Message]

class ChatRoomList(BaseModel):
    user_id: str
    chat_room_id: str
    chat_room_title: str
    total_chat_count: int
    created_at: str