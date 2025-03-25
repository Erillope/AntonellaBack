from core.common import SystemException

class ProductException(SystemException): ...


class InvalidProductNameException(ProductException):
    @classmethod
    def invalid_product_name(cls, name: str) -> 'InvalidProductNameException':
        return cls(f'El nombre del producto "{name}" no es válido')