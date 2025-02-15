from enum import Enum
from core.common import PatternMatcher
from .exceptions import InvalidServiceNameException
from typing import Optional, ClassVar
from pydantic import BaseModel
from core.common.image_storage import Base64ImageStorage

class ServiceType(Enum):
    HAIR = "CABELLO"
    SPA = "SPA"
    NAIL = "UÑAS"
    MAKEUP = "MAQUILLAJE"


class ServiceStatus(Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class InputType(Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"

    
class Choice(BaseModel):
    option: str
    image: Optional[Base64ImageStorage] = None


class ServiceName:
    REGREX = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÜüÑñ' &-]{3,50}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidServiceNameException.invalid_service_name(value)