from abc import ABC, abstractmethod
from datetime import timedelta
from .dto import (ServiceItemDto, UpdateServiceItemDto, FilterServiceItemByDto, EmployeeServiceInfoDto,
                  RequestEmployeeServiceInfoDto, UpdateOrderDto, FilterServiceItemResponseDto)
from ..domain.values import Payment, Progresstatus
from typing import List, Optional
from .mapper import ServiceItemMapper
from .repository import GetServiceItem
from .order_service import AbstractOrderService
from datetime import datetime

class AbstractServiceItemService(ABC):
    @abstractmethod
    def create_service_item(self, dto: ServiceItemDto, order_id: str) -> ServiceItemDto: ...
    
    @abstractmethod
    def get_service_items(self, order_id: str) -> List[ServiceItemDto]: ...
    
    @abstractmethod
    def update_service_item(self, dto: UpdateServiceItemDto) -> ServiceItemDto: ...
    
    @abstractmethod
    def delete_service_item(self, service_item_id: str) -> None: ...
    
    @abstractmethod
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> FilterServiceItemResponseDto: ...
    
    @abstractmethod
    def get_employee_service_info(self, dto: RequestEmployeeServiceInfoDto) -> EmployeeServiceInfoDto: ...


class ServiceItemService(AbstractServiceItemService):
    def __init__(self, get_service_item: GetServiceItem, order_service: AbstractOrderService) -> None:
        self._get_service_item = get_service_item
        self._order_service = order_service
    
    def get(self, service_item_id: str) -> ServiceItemDto:
        service_item = self._get_service_item.get(service_item_id)
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def create_service_item(self, dto: ServiceItemDto, order_id: str) -> ServiceItemDto:
        service_item = ServiceItemMapper.to_service_item(dto)
        service_item.set_order_id(order_id)
        if dto.payment_percentage:
            service_item.set_payment_percentage(dto.payment_percentage)
        if dto.date_info.end_time:
            service_item.date_info.set_end_time(dto.date_info.end_time)
        else:
            start_dt = datetime.combine(dto.date_info.day, service_item.date_info.start_time)
            end_time = (start_dt + timedelta(minutes=10)).time()
            service_item.date_info.set_end_time(end_time)
        start_dt = datetime.combine(dto.date_info.day, service_item.date_info.start_time)
        self._order_service.set_date(order_id, start_dt)
        service_item.save()
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def get_service_items(self, order_id: str) -> List[ServiceItemDto]:
        service_items = self._get_service_item.get_by_order_id(order_id)
        return [ServiceItemMapper.to_service_item_dto(item) for item in service_items]
    
    def update_service_item(self, dto: UpdateServiceItemDto) -> ServiceItemDto:
        service_item = self._get_service_item.get(dto.id)
        p: Optional[List[Payment]] = None
        if dto.payments:
            p = [Payment(employee_id=payment.employee_id) for payment in dto.payments]
            if dto.payment_percentage and dto.base_price:
                p = [
                    Payment.calculate(
                        employee_id=payment.employee_id,
                        base_price=dto.base_price*dto.payment_percentage,
                        percentage=payment.percentage
                    )     
                    for payment in dto.payments if payment.percentage is not None
                ]
        service_item.update_data(
            service_id=dto.service_id,
            payment_percentage=dto.payment_percentage,
            date_info=dto.date_info,
            status=dto.status,
            base_price=dto.base_price,
            payments=p
        )
        service_item.save()
        if dto.status and dto.status == Progresstatus.IN_PROGRESS:
            self._order_service.update_order(UpdateOrderDto(
                id=service_item.get_order_id(),
                progress_status=Progresstatus.IN_PROGRESS
            ))
        if dto.status and dto.status == Progresstatus.FINISHED:
            items = self._get_service_item.get_by_order_id(service_item.get_order_id())
            if all(item.status == Progresstatus.FINISHED for item in items):
                self._order_service.update_order(UpdateOrderDto(
                    id=service_item.get_order_id(),
                    progress_status=Progresstatus.FINISHED
                ))
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def delete_service_item(self, service_item_id: str) -> None:
        service_item = self._get_service_item.get(service_item_id)
        service_item.delete()
    
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> FilterServiceItemResponseDto:
        service_items, filtered_count = self._get_service_item.filter_service_items(filter_dto)
        total_count = self._get_service_item.total_count()
        return FilterServiceItemResponseDto(
            service_items=[ServiceItemMapper.to_service_item_dto(item) for item in service_items],
            total_count=total_count,
            filtered_count=filtered_count
        )

    def get_employee_service_info(self, dto: RequestEmployeeServiceInfoDto) -> EmployeeServiceInfoDto:
        service_items, _ = self._get_service_item.filter_service_items(
            FilterServiceItemByDto(
                start_date=dto.start_date,
                end_date=dto.end_date,
                employee_id=dto.employee_id,
                limit=dto.limit,
                offset=dto.offset
            )
        )
        return EmployeeServiceInfoDto(
            employee_id=dto.employee_id,
            start_date=dto.start_date,
            end_date=dto.end_date,
            total_facturado=self._get_service_item.get_employee_total_facturado(
                dto.employee_id, dto.start_date, dto.end_date
            ),
            total_pagado=self._get_service_item.get_employee_total_pagado(
                dto.employee_id, dto.start_date, dto.end_date
            ),
            service_items=[ServiceItemMapper.to_service_item_dto(item) for item in service_items]
        )