from core.common import SystemException

class StoreServiceException(SystemException): ...

class InvalidServiceNameException(StoreServiceException):
    @classmethod
    def invalid_service_name(cls, name: str) -> "InvalidServiceNameException":
        return cls(f"El nombre del servicio '{name}' es inválido")