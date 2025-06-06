from abc import ABC, abstractmethod
from .dto import CreateOrderDto, OrderDto, UpdateOrderDto
from ..domain.order import Order
from .mapper import OrderMapper
from typing import List
from core.common.abstract_repository import GetModel

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


class OrderService(AbstractOrderService):
    def __init__(self, get_order: GetModel[Order]) -> None:
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
            status=dto.status
        )
        order.save()
        return OrderMapper.to_order_dto(order)
    
    def delete_order(self, order_id: str) -> None:
        order = self._get_order.get(order_id)
        order.delete()
    
    def get_all(self) -> List[OrderDto]:
        orders = self._get_order.get_all()
        return [OrderMapper.to_order_dto(order) for order in orders]