from core.common import SystemException

class OrderException(SystemException): ...

class EmployeeAlreadyIsInServiceItem(OrderException):
    @classmethod
    def already_in_service_item(cls, employee_id: str) -> "EmployeeAlreadyIsInServiceItem":
        return cls(f"El empleado {employee_id} ya está en el item de servicio.")


class MissingPaymentPercentageException(OrderException):
    @classmethod
    def missing_payment_percentage(cls) -> "MissingPaymentPercentageException":
        return cls("Se requiere el porcentaje de pago.")


class MissingOrderIdException(OrderException):
    @classmethod
    def missing_order_id(cls) -> "MissingOrderIdException":
        return cls("Se requiere el ID del pedido.")