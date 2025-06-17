from __future__ import annotations
from core.common import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .order import Order
    from .item import ServiceItem, ProductItem

class OrderSaved(Event):
    def __init__(self, order: Order):
        self.order = order


class OrderDeleted(Event):
    def __init__(self, order_id: str):
        self.order_id = order_id


class ServiceItemSaved(Event):
    def __init__(self, service_item: ServiceItem):
        self.service_item = service_item


class ServiceItemDeleted(Event):
    def __init__(self, service_item_id: str):
        self.service_item_id = service_item_id


class ProductItemSaved(Event):
    def __init__(self, product_item: ProductItem):
        self.product_item = product_item
    

class ProductItemDeleted(Event):
    def __init__(self, product_item_id: str):
        self.product_item_id = product_item_id