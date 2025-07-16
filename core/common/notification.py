from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Optional

class NotificationType(str, Enum):
    INSTANTANEA = "INSTANTANEA"
    PROGRAMADA = "PROGRAMADA"

class NotificationMessage(BaseModel):
    title: str
    body: str
    user_id: str
    type: NotificationType = NotificationType.INSTANTANEA
    publish_date: Optional[datetime] = None

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: NotificationMessage) -> None: ...