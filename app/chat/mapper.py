from ..common.table_mapper import TableMapper
from .models import ChatMessageTable, ChatTable
from core.chat.chat import ChatMessage

class ChatMessageTableMapper(TableMapper[ChatMessageTable, ChatMessage]):
    def to_model(self, table: ChatMessageTable) -> ChatMessage:
        return ChatMessage(
            id=str(table.id),
            chat_id=str(table.chat_id),
            sender_id=str(table.sender.id),
            content=table.content,
            timestamp=table.timestamp,
            message_type=table.message_type
        )
    
    def to_table(self, model: ChatMessage) -> ChatMessageTable:
        return ChatMessageTable(
            id=model.id,
            chat=ChatTable.objects.get(id=model.chat_id),
            sender_id=model.sender_id,
            content=model.content,
            timestamp=model.timestamp,
            message_type=model.message_type
        )