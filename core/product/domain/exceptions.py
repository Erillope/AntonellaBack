from core.common import SystemException

class ProductException(SystemException): ...


class InvalidProductNameException(ProductException):
    @classmethod
    def invalid_product_name(cls, name: str) -> 'InvalidProductNameException':
        return cls(f'El nombre del producto "{name}" no es válido')


class CannotReduceStockException(ProductException):
    @classmethod
    def cannot_reduce_stock(cls, product_id: str, product_stock: int, quantity: int) -> 'CannotReduceStockException':
        return cls(f'No se puede reducir el producto con ID "{product_id}" que tiene un stock de "{product_stock}" al reducirlo en {quantity}. El stock es insuficiente para esta operación.')