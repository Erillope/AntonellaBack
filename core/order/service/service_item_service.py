from abc import ABC, abstractmethod
from .dto import ServiceItemDto, UpdateServiceItemDto
from ..domain.values import Payment
from typing import List
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


class ServiceItemService(AbstractServiceItemService):
    def __init__(self, get_service_item: GetServiceItem) -> None:
        self._get_service_item = get_service_item
    
    def create_service_item(self, dto: ServiceItemDto, order_id: str) -> ServiceItemDto:
        service_item = ServiceItemMapper.to_service_item(dto)
        service_item.set_order_id(order_id)
        service_item.save()
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def get_service_items(self, order_id: str) -> List[ServiceItemDto]:
        service_items = self._get_service_item.get_by_order_id(order_id)
        return [ServiceItemMapper.to_service_item_dto(item) for item in service_items]
    
    def update_service_item(self, dto: UpdateServiceItemDto) -> ServiceItemDto:
        service_item = self._get_service_item.get(dto.id)
        service_item.update_data(
            service_id=dto.service_id,
            payment_percentage=dto.payment_percentage,
            date_info=dto.date_info,
            status=dto.status,
            base_price=dto.base_price,
            payments=[
                Payment.calculate(
                    employee_id=payment.employee_id,
                    base_price=service_item.price.base_price,
                    percentage=payment.percentage
                ) for payment in dto.payments if payment.percentage is not None
            ]
        )
        service_item.save()
        return ServiceItemMapper.to_service_item_dto(service_item)
    
    def delete_service_item(self, service_item_id: str) -> None:
        service_item = self._get_service_item.get(service_item_id)
        service_item.delete()