from typing import Optional
from pydantic import BaseModel, validator

LLM_TYPE_KEYS = {
    'Claude v3 Haiku': 'haiku',
    'Claude V3 Opus': 'opus',
    'Claude V3 Sonnet': 'sonnet3',
    'Claude V3.5 Sonnet': 'sonnet35'
}

class MultiTurn(BaseModel):
    brand_name: str
    model_name: str
    error_code: Optional[str] = None
    input_query: Optional[str] = None
    parts_name: Optional[str] = None

class ChatRequest(BaseModel):
    llm: str
    message: str
    message_id: str
    session_id: str
    connection_id: str
    conversation_type: str
    knowledge_type: str = None
    multi_turn: Optional[MultiTurn] = None

    @validator("llm", pre=True, always=True)
    def set_model(cls, v):
        return LLM_TYPE_KEYS.get(v, 'haiku')
