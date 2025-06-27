from abc import ABC, abstractmethod
from .dto import ServiceItemDto, UpdateServiceItemDto, FilterServiceItemByDto, EmployeeServiceInfoDto, RequestEmployeeServiceInfoDto
from ..domain.values import Payment
from typing import List, Optional
from .mapper import ServiceItemMapper
from .repository import GetServiceItem

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
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> List[ServiceItemDto]: ...
    
    @abstractmethod
    def get_employee_service_info(self, dto: RequestEmployeeServiceInfoDto) -> EmployeeServiceInfoDto: ...


class ServiceItemService(AbstractServiceItemService):
    def __init__(self, get_service_item: GetServiceItem) -> None:
        self._get_service_item = get_service_item
    
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
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def delete_service_item(self, service_item_id: str) -> None:
        service_item = self._get_service_item.get(service_item_id)
        service_item.delete()
    
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> List[ServiceItemDto]:
        if filter_dto.client_id:
            self._get_service_item.prepare_client_id_filter(filter_dto.client_id)
        if filter_dto.start_date:
            self._get_service_item.prepare_start_date_filter(filter_dto.start_date)
        if filter_dto.end_date:
            self._get_service_item.prepare_end_date_filter(filter_dto.end_date)
        if filter_dto.status:
            self._get_service_item.prepare_status_filter(filter_dto.status)
        if filter_dto.service_id:
            self._get_service_item.prepare_service_id_filter(filter_dto.service_id)
        if filter_dto.employee_id:
            self._get_service_item.prepare_employee_id_filter(filter_dto.employee_id)
        service_items = self._get_service_item.get_filtered_service_items(
            limit=filter_dto.limit,
            offset=filter_dto.offset
        )
        return [ServiceItemMapper.to_service_item_dto(item) for item in service_items]
    
    def get_employee_service_info(self, dto: RequestEmployeeServiceInfoDto) -> EmployeeServiceInfoDto:
        self._get_service_item.prepare_employee_id_filter(dto.employee_id)
        self._get_service_item.prepare_start_date_filter(dto.start_date)
        self._get_service_item.prepare_end_date_filter(dto.end_date)
        service_items = self._get_service_item.get_filtered_service_items(dto.limit, dto.offset)
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