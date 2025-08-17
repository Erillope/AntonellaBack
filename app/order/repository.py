from core.order.service.repository import GetServiceItem, GetProductItem, GetOrder
from core.order.domain.item import ServiceItem, ProductItem
from core.order.domain.order import Order
from core.order.service.dto import FilterOrderDto, FilterServiceItemByDto, EmployeeCalendarDto
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from .mapper import ServiceItemTableMapper, OrderTableMapper, ProductItemTableMapper
from app.order.models import ServiceItemTable, OrderTable, ProductItemTable
from typing import List, Optional, Tuple
from core.common import EventSubscriber, Event
from core.order.domain.events import OrderSaved, OrderDeleted, ServiceItemSaved, ServiceItemDeleted, ProductItemSaved, ProductItemDeleted
from .models import PaymentTable, EmployeePaymentTable
from app.user.models import EmployeeAccountTableData
from django.db.models import Q, Sum
from datetime import date
from decimal import Decimal
from core.common.config import AppConfig

class DjangoGetOrder(DjangoGetModel[OrderTable, Order], GetOrder):
    def __init__(self) -> None:
        super().__init__(OrderTable, OrderTableMapper())

    def build_filter(self, dto: FilterOrderDto) -> Q:
        filter_conditions = Q()
        if dto.client_name:
            filter_conditions &= Q(client__name__icontains=dto.client_name)
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
        orders = OrderTable.objects.filter(_filter).distinct().order_by('-order_date')
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

    def get_employee_total_facturado(self, employee_id: str, start_date: Optional[date], end_date: Optional[date]) -> Decimal:
        _filter = Q(paymenttable__employee__id=employee_id)
        if start_date:
            _filter &= Q(date_info_day__gte=start_date)
        if end_date:
            _filter &= Q(date_info_day__lte=end_date)
        total_facturado = ServiceItemTable.objects.filter(_filter).aggregate(total=Sum('base_price'))['total'] or Decimal(0)
        return total_facturado

    def get_employee_total_por_pagar(self, employee_id: str, start_date: Optional[date], end_date: Optional[date]) -> Decimal:
        _filter = Q(employee__id=employee_id)
        total_por_pagar_salario = Decimal(0)
        if start_date:
            _filter &= Q(service_item__date_info_day__gte=start_date)
        if end_date:
            _filter &= Q(service_item__date_info_day__lte=end_date)
        total_por_pagar = PaymentTable.objects.filter(_filter).aggregate(total=Sum('amount'))['total'] or Decimal(0)
        
        if start_date and end_date:
            months = self._calculate_months(start_date, end_date)
            total_por_pagar_salario = AppConfig.salario() * months
            return total_por_pagar + total_por_pagar_salario

        if not start_date and not end_date:
            employee = EmployeeAccountTableData.objects.get(id=employee_id)
            months = self._calculate_months(employee.created_date, date.today())
            total_por_pagar_salario = AppConfig.salario() * months
            return total_por_pagar + total_por_pagar_salario
        
        if start_date:
            months = self._calculate_months(start_date, date.today())
            total_por_pagar_salario = AppConfig.salario() * months
            return total_por_pagar + total_por_pagar_salario
        if end_date:
            employee = EmployeeAccountTableData.objects.get(id=employee_id)
            months = self._calculate_months(employee.created_date, end_date)
            total_por_pagar_salario = AppConfig.salario() * months
            return total_por_pagar + total_por_pagar_salario

        return total_por_pagar
    
    def get_employee_total_pagado(self, employee_id: str) -> Decimal:
        total_pagado = EmployeePaymentTable.objects.filter(
            employee__id=employee_id
            ).aggregate(total=Sum('amount'))['total'] or Decimal(0)
        return total_pagado

    def _calculate_months(self, start_date: date, end_date: date) -> int:
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    def get_employee_calendar(self, employee_id: str) -> List[EmployeeCalendarDto]:
        calendar = []
        items = ServiceItemTable.objects.filter(
            paymenttable__employee__id=employee_id,
            order__status="confirmado",
            date_info_day__gte=date.today()
        )
        for item in items:
            calendar.append(EmployeeCalendarDto(
                day=item.date_info_day,
                start_time=item.date_info_start_time,
                end_time=item.date_info_end_time
            ))
        return calendar


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