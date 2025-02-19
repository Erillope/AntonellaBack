from enum import Enum
from core.common import PatternMatcher
from .exceptions import InvalidServiceNameException
from pydantic import BaseModel

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
    image_url: str
    
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