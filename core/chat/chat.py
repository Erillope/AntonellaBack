from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import datetime
from typing import ClassVar, Optional
from enum import Enum
from .events import ChatMessageSaved
from core.common.values import ID, GuayaquilDatetime
from core.common.image_storage import Base64ImageStorage, ImageSaved
from core.common import Event
from typing import List

class MessageType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    
class ChatMessage(BaseModel):
    chat_id: str
    id: str
    sender_id: str
    content: str
    timestamp: datetime
    message_type: MessageType
    IMAGE_PATH: ClassVar[str] = f'chat'
    readed_by_client: bool
    readed_by_admin: bool
    _events: List[Event] = PrivateAttr(default=[])
    
    @model_validator(mode='after')
    def init(self) -> 'ChatMessage':
        self._validate()
        return self
    
    def _validate(self) -> None:
        ID.validate(self.id)
        ID.validate(self.chat_id)
        ID.validate(self.sender_id)
        self.timestamp = GuayaquilDatetime.localize(self.timestamp)
        if self.message_type == MessageType.IMAGE:
            self.set_image(self.content)
    
    def set_image(self, image: str) -> None:
        '''Establece la foto de perfil de la cuenta de usuario'''
        if Base64ImageStorage.is_media_url(image):
            self.content = image
            return
        save_image = Base64ImageStorage(folder=self.IMAGE_PATH, base64_image=image)
        self.content = save_image.get_url()
        self._events.append(ImageSaved(images=[save_image]))
        
    def save(self) -> None:
        ChatMessageSaved(message=self).publish()
        for event in self._events:
            event.publish()