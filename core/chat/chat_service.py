from abc import ABC, abstractmethod
from .chat import ChatMessage
from .dto import AddMessageDto
from .repository import GetChatMessage
from datetime import datetime

class AbstractChatService(ABC):
    @abstractmethod
    def add_message(self, dto: AddMessageDto) -> ChatMessage: ...

    @abstractmethod
    def get_messages(self, chat_id: str, offset: int = 0, limit: int = 20) -> list[ChatMessage]: ...


class ChatService(AbstractChatService):
    def __init__(self, repository: GetChatMessage):
        self.repository = repository

    def add_message(self, dto: AddMessageDto) -> ChatMessage:
        message = ChatMessage(
            chat_id=dto.chat_id,
            sender_id=dto.sender_id,
            content=dto.content,
            timestamp=datetime.now(),
            message_type=dto.message_type
        )
        message.save()
        return message

    def get_messages(self, chat_id: str, offset: int = 0, limit: int = 20) -> list[ChatMessage]:
        return self.repository.get_chat_history(chat_id, offset, limit)


