from pydantic import BaseModel
from abc import ABC, abstractmethod

class NotificationMessage(BaseModel):
    title: str
    body: str
    user_id: str

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: NotificationMessage) -> None: ...