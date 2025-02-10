# from typing import Optional
from pydantic import BaseModel, validator

LLM_TYPE_KEYS = {
    'Claude v3 Haiku': 'haiku',
    'Claude V3 Opus': 'opus',
    'Claude V3 Sonnet': 'sonnet3',
    'Claude V3.5 Sonnet': 'sonnet35'
}

class ChatRequest(BaseModel):
    llm: str
    message: str
    conversation_type: str
    user_id: str
    session_id: str
    message_id: int
    chat_room_id: str
    # chat_room_exist: bool

    @validator("llm", pre=True, always=True)
    def set_model(cls, v):
        return LLM_TYPE_KEYS.get(v, 'haiku')
