from pydantic import BaseModel
from .chat import MessageType

class AddMessageDto(BaseModel):
    chat_id: str
    sender_id: str
    content: str
    message_type: MessageType