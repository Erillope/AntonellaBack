from pydantic import BaseModel
from enum import Enum
import uuid
import re
from .exceptions import InvalidOrderDirectionException, InvalidIdException, InvalidAmount
from decimal import Decimal

class ID:
    '''Validador y generador de UUIDs'''
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.is_id(value):
            raise InvalidIdException.invalid_id(value)
    
    @classmethod
    def generate(cls) -> str:
        return str(uuid.uuid4())
    
    @classmethod
    def is_id(cls, value: str) -> bool:
        try:
            uuid.UUID(value)
            return True
        except:
            return False


class PatternMatcher(BaseModel):
    '''Validador de patrones de texto'''
    pattern: str
    
    def match(self, value: str) -> bool:
        return bool(re.match(self.pattern, value.encode('utf-8').decode('utf-8')))


class OrdenDirection(Enum):
    '''Dirección de ordenamiento para filtros'''
    ASC = "ASC"
    DESC = "DESC"

    @classmethod
    def from_name(cls, name: str) -> "OrdenDirection":
        if name in cls._member_names_:
            return cls(name)
        raise InvalidOrderDirectionException.invalid_direction(name)


class AmountValue:
    @classmethod
    def validate(cls, value: Decimal) -> None:
        if value < 0:
            raise InvalidAmount.invalid_amount(value)