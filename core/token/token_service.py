from abc import ABC, abstractmethod
from .tokens import Token
from datetime import timedelta
from core.common.abstract_repository import GetModel
from .exceptions import InvalidTokenException

class AbstractTokenService(ABC):
    @abstractmethod
    def exists(self, id: str) -> bool: ...

    @abstractmethod
    def get(self, id: str) -> Token: ...

    @abstractmethod
    def create(self, expires: timedelta, user_id: str) -> Token: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...
    
    @abstractmethod
    def clear_expired(self) -> None: ...


class TokenService(AbstractTokenService):
    def __init__(self, get_token: GetModel[Token]):
        self.get_token = get_token
        
    def exists(self, id: str) -> bool:
        if not self.get_token.exists(id): return False
        token = self.get_token.get(id)
        return not token.is_expired()
    
    def get(self, id: str) -> Token:
        if self.exists(id):
            return self.get_token.get(id)
        raise InvalidTokenException.invalid(id)
    
    def create(self, expires: timedelta, user_id: str) -> Token:
        token = Token.generate(expires, user_id)
        token.save()
        return token
    
    def delete(self, id: str) -> None:
        token = self.get_token.get(id)
        token.delete()
    
    def clear_expired(self) -> None:
        for token in self.get_token.get_all():
            if token.is_expired():
                token.delete()