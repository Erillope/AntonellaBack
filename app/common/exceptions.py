from core.common import SystemException
from typing import List

class InvalidFieldException(SystemException):
    @classmethod
    def invalid_field(cls, field: str, fields: List[str]) -> "InvalidFieldException":
        return cls(f"El campo '{field}' es inválido. Los campos válidos son: {fields}")

class MissingOperationException(SystemException):
    @classmethod
    def missing_operation(cls, operations: List[str]) -> "MissingOperationException":
        return cls(f"'Falta la operación. Las operaciones disponibles son {operations}")