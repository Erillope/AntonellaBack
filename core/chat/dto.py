from pydantic import BaseModel
from .chat import MessageType
from typing import Optional

class AddMessageDto(BaseModel):
    chat_id: str
    sender_id: str
    content: str
    message_type: MessageType
    readed_by_client: bool
    readed_by_admin: bool


class UserChatDto(BaseModel):
    user_id: str
    user_name: str
    user_photo: Optional[str] = None