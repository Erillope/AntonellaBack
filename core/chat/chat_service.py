from abc import ABC, abstractmethod
from .chat import ChatMessage
from .dto import AddMessageDto, UserChatDto
from .repository import GetChatMessage
from datetime import datetime
from core.common import ID

class AbstractChatService(ABC):
    @abstractmethod
    def add_message(self, dto: AddMessageDto) -> ChatMessage: ...

    @abstractmethod
    def get_messages(self, chat_id: str, offset: int = 0, limit: int = 20) -> list[ChatMessage]: ...
    
    @abstractmethod
    def get_user_chats(self) -> list[UserChatDto]: ...


class ChatService(AbstractChatService):
    def __init__(self, repository: GetChatMessage):
        self.repository = repository

    def add_message(self, dto: AddMessageDto) -> ChatMessage:
        message = ChatMessage(
            id = ID.generate(),
            chat_id=dto.chat_id,
            sender_id=dto.sender_id,
            content=dto.content,
            timestamp=datetime.now(),
            message_type=dto.message_type
        )
        message.save()
        return message

    def get_messages(self, user_id: str, offset: int = 0, limit: int = 20) -> list[ChatMessage]:
        return self.repository.get_chat_history(user_id, offset, limit)
    
    def get_user_chats(self) -> list[UserChatDto]:
        return self.repository.get_user_chats()


