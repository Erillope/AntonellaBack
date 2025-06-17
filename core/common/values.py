from pydantic import BaseModel
from enum import Enum
import uuid
import re
import rstr
import string
import random
from .exceptions import InvalidOrderDirectionException, InvalidIdException, InvalidAmount
from decimal import Decimal
import pytz
from datetime import datetime

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
    
    def generate(self) -> str:
        while True:
            generated = rstr.xeger(self.pattern)
            if re.fullmatch(self.pattern, generated):
                return generated
    
    def random(self, long: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=long))
    
    def generate_invalid(self, long: int) -> str:
        while True:
            s = ''.join(random.choices(string.ascii_letters + string.digits, k=long))
            if not re.fullmatch(self.pattern, s):
                return s


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
    def validate(cls, value: Decimal | int) -> None:
        if value < 0:
            raise InvalidAmount.invalid_amount(value)
    
    @classmethod
    def validate_percentage(cls, value: Decimal) -> None:
        if value < 0 or value > 1:
            raise InvalidAmount.invalid_percentage(value)


class GuayaquilDatetime:
    timezone = pytz.timezone("America/Guayaquil")
    
    @classmethod
    def now(cls) -> datetime:
        return cls.timezone.localize(datetime.now())
    
    @classmethod
    def localize(cls, datetime: datetime) -> datetime:
        if datetime.tzinfo is None:
            return cls.timezone.localize(datetime)
        return datetime.astimezone(cls.timezone)