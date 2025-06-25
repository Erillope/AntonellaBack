from core.chat.repository import GetChatMessage
from .mapper import ChatMessageTableMapper
from typing import List
from app.common.django_repository import DjangoSaveModel, DjangoGetModel
from core.common import EventSubscriber, Event
from core.chat.chat import ChatMessage
from .models import ChatMessageTable, ChatTable
from core.chat.events import ChatMessageSaved
from core.user.domain.events import UserAccountSaved
from core.user.domain.user import EmployeeAccount
from core.common import ID

class DjangoGetChatMessage(DjangoGetModel[ChatMessageTable, ChatMessage], GetChatMessage):
    def __init__(self) -> None:
        super().__init__(ChatMessageTable ,ChatMessageTableMapper())
    
    def get_chat_history(self, user_id: str, offset: int, limit: int) -> List[ChatMessage]:
        chat = ChatTable.objects.filter(user__id=user_id).first()
        tables = ChatMessageTable.objects.filter(chat_id=chat.id).order_by('-timestamp')[offset:offset + limit]
        return [self.mapper.to_model(table) for table in tables]

class DjangoChatMessageSaved(DjangoSaveModel[ChatMessageTable, ChatMessage], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ChatMessageTableMapper())
        EventSubscriber.__init__(self)
        
    def create_chat(self, user_id: str) -> None:
        if ChatTable.objects.filter(user_id=user_id).exists():
            return
        ChatTable.objects.create(user_id=user_id, id=ID.generate())
        
    def handle(self, event: Event) -> None:
        if isinstance(event, ChatMessageSaved):
            self.save(event.message)
        if isinstance(event, UserAccountSaved) and not isinstance(event.user, EmployeeAccount):
            self.create_chat(event.user.id)
        
        
    