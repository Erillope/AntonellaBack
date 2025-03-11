from abc import ABC, abstractmethod
from pydantic import BaseModel

class EmailMessage(BaseModel):
    to: str
    subject: str
    body: str
    
    
class EmailHost(ABC):
    @abstractmethod
    def send_email(self, message: EmailMessage) -> None: ...
    
    @abstractmethod
    def set_host(self, email_host: str, password: str) -> None: ...