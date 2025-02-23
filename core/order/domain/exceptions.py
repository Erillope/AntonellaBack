from core.common import SystemException

class OrderException(SystemException): ...

class EmployeeAlreadyIsInServiceItem(OrderException):
    @classmethod
    def already_in_service_item(cls, employee_id: str) -> "EmployeeAlreadyIsInServiceItem":
        return cls(f"El empleado {employee_id} ya está en el item de servicio.")