from pydantic import BaseModel, model_validator
from datetime import datetime, timedelta
from core.common.values import ID, GuayaquilDatetime
from core.common.events import Event

class Token(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    expired_at: datetime
    
    @model_validator(mode='after')
    def init(self) -> 'Token':
        self.created_at = GuayaquilDatetime.localize(self.created_at)
        self.expired_at = GuayaquilDatetime.localize(self.expired_at)
        return self
    
    def is_expired(self) -> bool:
        return GuayaquilDatetime.now() > self.expired_at
    
    @classmethod
    def generate(cls, expires: timedelta, user_id: str) -> 'Token':
        return cls(
            id=ID.generate(),
            user_id=user_id,
            created_at=datetime.now(),
            expired_at=datetime.now() + expires
        )
    
    def save(self) -> None:
        CreatedToken(self).publish()
    
    def delete(self) -> None:
        DeletedToken(self.id).publish()


class CreatedToken(Event):    
    def __init__(self, token: Token):
        self.token = token
        super().__init__()


class DeletedToken(Event):
    def __init__(self, token_id: str):
        self.token_id = token_id
        super().__init__()