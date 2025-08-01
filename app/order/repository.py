from core.order.service.repository import GetServiceItem, GetProductItem, GetOrder
from core.order.domain.item import ServiceItem, ProductItem
from core.order.domain.order import Order
from core.order.service.dto import FilterOrderDto, FilterServiceItemByDto
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from .mapper import ServiceItemTableMapper, OrderTableMapper, ProductItemTableMapper
from app.order.models import ServiceItemTable, OrderTable, ProductItemTable
from typing import List, Optional, Tuple
from core.common import EventSubscriber, Event
from core.order.domain.events import OrderSaved, OrderDeleted, ServiceItemSaved, ServiceItemDeleted, ProductItemSaved, ProductItemDeleted
from .models import PaymentTable
from app.user.models import EmployeeAccountTableData
from django.db.models import Q, Sum
from datetime import date
from decimal import Decimal

class DjangoGetOrder(DjangoGetModel[OrderTable, Order], GetOrder):
    def __init__(self) -> None:
        super().__init__(OrderTable, OrderTableMapper())

    def build_filter(self, dto: FilterOrderDto) -> Q:
        filter_conditions = Q()
        if dto.client_id:
            filter_conditions &= Q(client__id=dto.client_id)
        if dto.status:
            filter_conditions &= Q(status=dto.status.value.lower())
        if dto.progress_status:
            filter_conditions &= Q(progress_status=dto.progress_status.value.lower())
        if dto.service_type:
            filter_conditions &= Q(serviceitemtable__service__type=dto.service_type.value.lower())
        if dto.start_date:
            filter_conditions &= Q(order_date__gte=dto.start_date)
        if dto.end_date:
            filter_conditions &= Q(order_date__lte=dto.end_date)
        return filter_conditions
    
    def filter_orders(self, dto: FilterOrderDto) -> Tuple[List[Order], int]:
        _filter = self.build_filter(dto)
        orders = OrderTable.objects.filter(_filter).distinct()
        orders_count = orders.count()
        if dto.only_count: return [], orders_count
        if dto.limit and dto.offset is not None:
            orders = orders[dto.offset:dto.offset + dto.limit]
        elif dto.limit:
            orders = orders[:dto.limit]
        elif dto.offset is not None:
            orders = orders[dto.offset:]
        return [self.mapper.to_model(order) for order in orders], orders_count

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
        self.filter_conditions = Q()

    def get_by_order_id(self, order_id: str) -> List[ServiceItem]:
        service_item_tables = ServiceItemTable.objects.filter(order__id=order_id)
        return [self.mapper.to_model(item) for item in service_item_tables]
    
    def build_filter(self, filter_dto: FilterServiceItemByDto) -> Q:
        filter_conditions = Q()
        if filter_dto.start_date:
            filter_conditions &= Q(date_info_day__gte=filter_dto.start_date)
        if filter_dto.end_date:
            filter_conditions &= Q(date_info_day__lte=filter_dto.end_date)
        if filter_dto.client_id:
            filter_conditions &= Q(order__client__id=filter_dto.client_id)
        if filter_dto.status:
            filter_conditions &= Q(status=filter_dto.status.value.lower())
        if filter_dto.service_id:
            filter_conditions &= Q(service__id=filter_dto.service_id)
        if filter_dto.employee_id:
            filter_conditions &= Q(paymenttable__employee__id=filter_dto.employee_id)
        return filter_conditions
    
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> Tuple[List[ServiceItem], int]:
        self.filter_conditions = self.build_filter(filter_dto)
        service_item_tables = ServiceItemTable.objects.filter(self.filter_conditions).distinct()
        filtered_count = service_item_tables.count()
        if filter_dto.only_count:
            return [], filtered_count
        if filter_dto.limit and filter_dto.offset:
            service_item_tables = service_item_tables[filter_dto.offset:filter_dto.offset + filter_dto.limit]
        elif filter_dto.limit:
            service_item_tables = service_item_tables[:filter_dto.limit]
        elif filter_dto.offset is not None:
            service_item_tables = service_item_tables[filter_dto.offset:]
        return [self.mapper.to_model(item) for item in service_item_tables], filtered_count

    def get_employee_total_facturado(self, employee_id: str, start_date: date, end_date: date) -> Decimal:
        total_facturado = ServiceItemTable.objects.filter(
            paymenttable__employee__id=employee_id,
            date_info_day__gte=start_date,
            date_info_day__lte=end_date
        ).aggregate(total=Sum('base_price'))['total'] or Decimal(0)
        return total_facturado

    def get_employee_total_pagado(self, employee_id: str, start_date: date, end_date: date) -> Decimal:
        total_pagado = PaymentTable.objects.filter(
            employee__id=employee_id,
            service_item__date_info_day__gte=start_date,
            service_item__date_info_day__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal(0)
        return total_pagado


class DjangoSaveServiceItem(DjangoSaveModel[ServiceItemTable, ServiceItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ServiceItemTableMapper())
        EventSubscriber.__init__(self)

    def save(self, model: ServiceItem) -> None:
        super().save(model)
        for payment in model.payments:
            PaymentTable.objects.filter(employee__id=payment.employee_id, service_item__id=model.id).delete()
            PaymentTable.objects.create(
                employee=EmployeeAccountTableData.objects.get(id=payment.employee_id),
                percentage=payment.percentage,
                amount=payment.amount,
                service_item=ServiceItemTable.objects.get(id=model.id)
            )
        
    
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


class DjangoGetProductItem(DjangoGetModel[ProductItemTable, ProductItem], GetProductItem):
    def __init__(self) -> None:
        super().__init__(ProductItemTable, ProductItemTableMapper())

    def get_by_order_id(self, order_id: str) -> List[ProductItem]:
        product_item_tables = ProductItemTable.objects.filter(order__id=order_id)
        return [self.mapper.to_model(item) for item in product_item_tables]


class DjangoSaveProductItem(DjangoSaveModel[ProductItemTable, ProductItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ProductItemTableMapper())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ProductItemSaved):
            self.save(event.product_item)


class DjangoDeleteProductItem(DjangoDeleteModel[ProductItemTable, ProductItem], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ProductItemTable, ProductItemTableMapper(), DjangoGetProductItem())
        EventSubscriber.__init__(self)

    def handle(self, event: Event) -> None:
        if isinstance(event, ProductItemDeleted):
            self.delete(event.product_item_id)