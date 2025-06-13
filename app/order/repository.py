from core.order.service.repository import GetServiceItem
from core.order.domain.item import ServiceItem
from core.order.domain.order import Order
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from .mapper import ServiceItemTableMapper, OrderTableMapper
from app.order.models import ServiceItemTable, OrderTable
from typing import List
from core.common import EventSubscriber, Event
from core.order.domain.events import OrderSaved, OrderDeleted, ServiceItemSaved, ServiceItemDeleted

class DjangoGetOrder(DjangoGetModel[OrderTable, Order]):
    def __init__(self) -> None:
        super().__init__(OrderTable, OrderTableMapper())


class DjangoSaveOrder(DjangoSaveModel[OrderTable, Order], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(OrderTableMapper())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, OrderSaved):
            self.save(event.order)


class DjangoDeleteOrder(DjangoDeleteModel[OrderTable, Order], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(OrderTable, OrderTableMapper(), DjangoGetOrder())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, OrderDeleted):
            self.delete(event.order_id)


class DjangoGetServiceItem(DjangoGetModel[ServiceItemTable, ServiceItem], GetServiceItem):
    def __init__(self) -> None:
        super().__init__(ServiceItemTable, ServiceItemTableMapper())

    def get_by_order_id(self, order_id: str) -> List[ServiceItem]:
        service_item_tables = ServiceItemTable.objects.filter(order__id=order_id)
        return [self.mapper.to_model(item) for item in service_item_tables]


class DjangoSaveServiceItem(DjangoSaveModel[ServiceItemTable, ServiceItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ServiceItemTableMapper())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ServiceItemSaved):
            self.save(event.service_item)


class DjangoDeleteServiceItem(DjangoDeleteModel[ServiceItemTable, ServiceItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ServiceItemTable, ServiceItemTableMapper(), DjangoGetServiceItem())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ServiceItemDeleted):
            self.delete(event.service_item_id)