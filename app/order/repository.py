from core.order.service.repository import GetServiceItem, GetProductItem
from core.order.domain.item import ServiceItem, ProductItem
from core.order.domain.order import Order
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from .mapper import ServiceItemTableMapper, OrderTableMapper, ProductItemTableMapper
from app.order.models import ServiceItemTable, OrderTable, ProductItemTable
from typing import List, Optional
from core.common import EventSubscriber, Event
from core.order.domain.events import OrderSaved, OrderDeleted, ServiceItemSaved, ServiceItemDeleted, ProductItemSaved, ProductItemDeleted
from .models import PaymentTable
from app.user.models import EmployeeAccountTableData
from django.db.models import Q, Sum
from datetime import date
from decimal import Decimal

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
        self.filter_conditions = Q()

    def get_by_order_id(self, order_id: str) -> List[ServiceItem]:
        service_item_tables = ServiceItemTable.objects.filter(order__id=order_id)
        return [self.mapper.to_model(item) for item in service_item_tables]
    
    def prepare_client_id_filter(self, client_id: str) -> None:
        self.filter_conditions &= Q(order__client__id=client_id)
    
    def prepare_start_date_filter(self, start_date: date) -> None:
        self.filter_conditions &= Q(date_info_day__gte=start_date)
    
    def prepare_end_date_filter(self, end_date: date) -> None:
        self.filter_conditions &= Q(date_info_day__lte=end_date)
    
    def prepare_status_filter(self, status: str) -> None:
        self.filter_conditions &= Q(status=status)
    
    def prepare_service_id_filter(self, service_id: str) -> None:
        self.filter_conditions &= Q(service__id=service_id)
    
    def prepare_employee_id_filter(self, employee_id: str) -> None:
        self.filter_conditions &= Q(paymenttable__employee__id=employee_id)
    
    def get_filtered_service_items(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ServiceItem]:
        service_item_tables = ServiceItemTable.objects.filter(self.filter_conditions).distinct()
        if limit and offset:
            service_item_tables = service_item_tables[offset:offset + limit]
        elif limit:
            service_item_tables = service_item_tables[:limit]
        elif offset:
            service_item_tables = service_item_tables[offset:]
        self.filter_conditions = Q()
        return [self.mapper.to_model(item) for item in service_item_tables]

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