from core.common import PatternMatcher
from .exceptions import InvalidProductNameException
from enum import Enum

class ProductStatus(str, Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    
class ProductName:
    REGREX = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÜüÑñ' &-]{3,50}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidProductNameException.invalid_product_name(value)