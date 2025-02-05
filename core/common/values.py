from pydantic import BaseModel
from enum import Enum
import uuid
import re
from .exceptions import InvalidOrderDirectionException, InvalidIdException

class ID:
    '''Validador y generador de UUIDs'''
    @staticmethod
    def validate(value: str) -> None:
        try:
            uuid.UUID(value)
        except:
            raise InvalidIdException.invalid_id(value)
    
    @staticmethod
    def generate() -> str:
        return str(uuid.uuid4())


class PatternMatcher(BaseModel):
    '''Validador de patrones de texto'''
    pattern: str
    
    def match(self, value: str) -> bool:
        return bool(re.match(self.pattern, value))


class OrdenDirection(Enum):
    '''Dirección de ordenamiento para filtros'''
    ASC = "ASC"
    DESC = "DESC"

    @classmethod
    def from_name(cls, name: str) -> "OrdenDirection":
        if name in cls._member_names_:
            return cls(name)
        raise InvalidOrderDirectionException.invalid_direction(name)