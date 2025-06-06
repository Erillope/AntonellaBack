from core.order.service.repository import GetServiceItem
from core.order.domain.item import ServiceItem
from core.order.domain.order import Order
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from .mapper import ServiceItemMapper, OrderMapper
from app.order.models import ServiceItemTable, OrderTableData
from typing import List
from core.common import EventSubscriber, Event
from core.order.domain.events import OrderSaved, OrderDeleted, ServiceItemSaved, ServiceItemDeleted

class DjangoGetOrder(DjangoGetModel[OrderTableData, Order]):
    def __init__(self) -> None:
        super().__init__(OrderTableData, OrderMapper())


class DjangoSaveOrder(DjangoSaveModel[OrderTableData, Order], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(OrderMapper())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, OrderSaved):
            self.save(event.order)


class DjangoDeleteOrder(DjangoDeleteModel[OrderTableData, Order], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(OrderTableData, OrderMapper(), DjangoGetOrder())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, OrderDeleted):
            self.delete(event.order_id)


class DjangoGetServiceItem(DjangoGetModel[ServiceItemTable, ServiceItem], GetServiceItem):
    def __init__(self) -> None:
        super().__init__(ServiceItemTable, ServiceItemMapper())

    def get_by_order_id(self, order_id: str) -> List[ServiceItem]:
        service_item_tables = ServiceItemTable.objects.filter(order__id=order_id)
        return [self.mapper.to_model(item) for item in service_item_tables]


class DjangoSaveServiceItem(DjangoSaveModel[ServiceItemTable, ServiceItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ServiceItemMapper())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ServiceItemSaved):
            self.save(event.service_item)


class DjangoDeleteServiceItem(DjangoDeleteModel[ServiceItemTable, ServiceItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ServiceItemTable, ServiceItemMapper(), DjangoGetServiceItem())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ServiceItemDeleted):
            self.delete(event.service_item_id)