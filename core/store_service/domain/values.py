from enum import Enum
from core.common import PatternMatcher
from .exceptions import InvalidServiceNameException, InvalidPriceRangeException
from pydantic import BaseModel, model_validator
from decimal import Decimal

class ServiceType(str, Enum):
    HAIR = "CABELLO"
    SPA = "SPA"
    NAIL = "UÑAS"
    MAKEUP = "MAQUILLAJE"


class ServiceStatus(str, Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class InputType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"

    
class Choice(BaseModel):
    option: str
    image: str
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Choice): return False
        return self.option == value.option


class ServiceName:
    REGREX = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÜüÑñ' &-]{3,50}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidServiceNameException.invalid_service_name(value)


class PriceRange(BaseModel):
    min: Decimal
    max: Decimal
    
    @model_validator(mode='after')
    def init(self) -> 'PriceRange':
        if self.min < 0 or self.max < 0:
            InvalidPriceRangeException.invalid_price_range(self.min, self.max)
        if self.min > self.max:
            InvalidPriceRangeException.invalid_price_range(self.min, self.max)
        return self


class Price(BaseModel):
    name: str
    range: PriceRange
    
    @classmethod
    def build(cls, name: str, min: Decimal, max: Decimal) -> 'Price':
        return cls(name=name, range=PriceRange(min=min, max=max))