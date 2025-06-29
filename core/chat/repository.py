from core.common.abstract_repository import GetModel
from abc import ABC, abstractmethod
from .chat import ChatMessage
from typing import List

class GetChatMessage(GetModel[ChatMessage], ABC):
    @abstractmethod
    def get_chat_history(self, chat_id: str, offset: int, limit: int) -> List[ChatMessage]: ...