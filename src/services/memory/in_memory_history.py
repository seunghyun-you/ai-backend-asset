from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    max_messages: int = 5
    
    class Config:
        arbitrary_types_allowed = True

    """In memory implementation of chat message history."""

    def clear(self) -> None:
        self.messages = []

    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)
        self.messages = self.messages[-self.max_messages:]
