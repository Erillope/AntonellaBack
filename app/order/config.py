from .repository import DjangoGetServiceItem, DjangoSaveServiceItem, DjangoDeleteServiceItem, DjangoGetOrder, DjangoSaveOrder, DjangoDeleteOrder
from core.order.service.order_service import OrderService
from core.order.service.service_item_service import ServiceItemService

get_order = DjangoGetOrder()

save_order = DjangoSaveOrder()

delete_order = DjangoDeleteOrder()

get_service_item = DjangoGetServiceItem()

save_service_item = DjangoSaveServiceItem()

delete_service_item = DjangoDeleteServiceItem()

service_item_service = ServiceItemService(get_service_item)

order_service = OrderService(get_order)