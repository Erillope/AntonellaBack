from __future__ import annotations
from core.common import Event
from core.common.image_storage import ImageDeleted
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .chat import ChatMessage, MessageType
    
class ChatMessageSaved(Event):
    '''Evento para cuando un mensaje de chat es guardado'''
    def __init__(self, message: ChatMessage):
        self.message = message