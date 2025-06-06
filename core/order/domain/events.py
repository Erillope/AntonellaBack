from __future__ import annotations
from core.common import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .order import Order
    from .item import ServiceItem

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