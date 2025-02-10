from enum import Enum
from core.common import PatternMatcher
from .exceptions import InvalidServiceNameException

class ServiceType(Enum):
    HAIR = "CABELLO"
    SPA = "SPA"
    NAIL = "UÑAS"
    MAKEUP = "MAQUILLAJE"


class ServiceStatus(Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class ServiceName:
    REGREX = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÜüÑñ' -]{3,50}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidServiceNameException.invalid_service_name(value)