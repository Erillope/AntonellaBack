from .repository import DjangoGetServiceItem, DjangoSaveServiceItem, DjangoDeleteServiceItem, DjangoGetOrder, DjangoSaveOrder, DjangoDeleteOrder, DjangoGetProductItem, DjangoSaveProductItem, DjangoDeleteProductItem
from core.order.service.order_service import OrderService
from core.order.service.service_item_service import ServiceItemService
from core.order.service.product_item_service import ProductItemService
from app.product.config import product_service

get_order = DjangoGetOrder()

save_order = DjangoSaveOrder()

delete_order = DjangoDeleteOrder()

get_service_item = DjangoGetServiceItem()

save_service_item = DjangoSaveServiceItem()

delete_service_item = DjangoDeleteServiceItem()

get_product_item = DjangoGetProductItem()

save_product_item = DjangoSaveProductItem()

delete_product_item = DjangoDeleteProductItem()

product_item_service = ProductItemService(get_product_item, product_service)

service_item_service = ServiceItemService(get_service_item)

order_service = OrderService(get_order)