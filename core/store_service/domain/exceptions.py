from core.common import SystemException

class StoreServiceException(SystemException): ...

class InvalidServiceNameException(StoreServiceException):
    @classmethod
    def invalid_service_name(cls, name: str) -> "InvalidServiceNameException":
        return cls(f"El nombre del servicio '{name}' es inválido")


class MissingStoreServiceException(StoreServiceException):
    @classmethod
    def not_asigned(cls) -> "MissingStoreServiceException":
        return cls("La pregunta de formulario no tiene un servicio de tienda asignado")
    

class OptionAlreadyExistsException(StoreServiceException):
    '''Excepción para cuando una opción de pregunta ya existe'''
    @classmethod
    def already_exists(cls, option: str) -> 'OptionAlreadyExistsException':
        return cls(f'La opción "{option}" ya existe')