from core.common import SystemException
from typing import List

class DjangoAppException(SystemException): ...

class InvalidFieldException(DjangoAppException):
    @classmethod
    def invalid_field(cls, field: str, fields: List[str]) -> "InvalidFieldException":
        return cls(f"El campo '{field}' es inválido. Los campos válidos son: {fields}")

class MissingOperationException(DjangoAppException):
    @classmethod
    def missing_operation(cls, operations: List[str]) -> "MissingOperationException":
        return cls(f"'Falta la operación. Las operaciones disponibles son {operations}")


class ModelNotFoundException(DjangoAppException):
    @classmethod
    def not_found(cls, model: str) -> "ModelNotFoundException":
        return cls(f"{model} no se encuentra registrado")