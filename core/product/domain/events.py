from __future__ import annotations
from core.common import Event
from core.common.image_storage import ImageDeleted
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .product import Product

class ProductSaved(Event):
    '''Evento para cuando un producto es actualizado'''
    def __init__(self, product: Product):
        self.product = product


class ProductDeleted(ImageDeleted):
    '''Evento para cuando un producto es eliminado'''
    def __init__(self, product: Product):
        super().__init__(product.images)
        self.product = product