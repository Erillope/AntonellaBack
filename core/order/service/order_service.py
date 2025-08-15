from abc import ABC, abstractmethod
from .dto import CreateOrderDto, OrderDto, UpdateOrderDto, FilterOrderDto, FilterOrderResponseDto
from .repository import GetOrder
from .mapper import OrderMapper
from typing import List
from ..domain.values import OrderStatusInfo
from datetime import datetime
from core.common import GuayaquilDatetime

class AbstractOrderService(ABC):
    @abstractmethod
    def create_order(self, dto: CreateOrderDto) -> OrderDto: ...

    @abstractmethod
    def get_order(self, order_id: str) -> OrderDto: ...

    @abstractmethod
    def update_order(self, dto: UpdateOrderDto) -> OrderDto: ...

    @abstractmethod
    def delete_order(self, order_id: str) -> None: ...

    @abstractmethod
    def get_all(self) -> List[OrderDto]: ...

    @abstractmethod
    def set_date(self, order_id: str, date: datetime) -> OrderDto: ...

    @abstractmethod
    def filter_orders(self, dto: FilterOrderDto) -> FilterOrderResponseDto: ...


class OrderService(AbstractOrderService):
    def __init__(self, get_order: GetOrder) -> None:
        self._get_order = get_order
    
    def create_order(self, dto: CreateOrderDto) -> OrderDto:
        order = OrderMapper.to_order(dto)
        order.save()
        return OrderMapper.to_order_dto(order)
    
    def get_order(self, order_id: str) -> OrderDto:
        order = self._get_order.get(order_id)
        return OrderMapper.to_order_dto(order)
    
    def update_order(self, dto: UpdateOrderDto) -> OrderDto:
        order = self._get_order.get(dto.id)
        order.update_data(
            client_id=dto.client_id,
            iva=dto.iva,
            status=OrderStatusInfo(
                status=dto.status if dto.status else order.status.status,
                progress_status=dto.progress_status if dto.progress_status else order.status.progress_status,
                payment_status=dto.payment_status if dto.payment_status else order.status.payment_status,
                payment_type=dto.payment_type if dto.payment_type else order.status.payment_type,
                client_confirmed=dto.client_confirmed if dto.client_confirmed is not None else order.status.client_confirmed,
            )
        )
        order.save()
        return OrderMapper.to_order_dto(order)
    
    def delete_order(self, order_id: str) -> None:
        order = self._get_order.get(order_id)
        order.delete()
    
    def get_all(self) -> List[OrderDto]:
        orders = self._get_order.get_all()
        return [OrderMapper.to_order_dto(order) for order in orders]
    
    def filter_orders(self, dto: FilterOrderDto) -> FilterOrderResponseDto:
        orders, filtered_count = self._get_order.filter_orders(dto)
        total_count = self._get_order.total_count()
        order_dtos = [OrderMapper.to_order_dto(order) for order in orders]
        return FilterOrderResponseDto(orders=order_dtos, total_count=total_count, filtered_count=filtered_count)
        
    
    def set_date(self, order_id: str, date: datetime) -> OrderDto:
        order = self._get_order.get(order_id)
        order.order_date = GuayaquilDatetime.localize(date)
        order.save()
        return OrderMapper.to_order_dto(order)