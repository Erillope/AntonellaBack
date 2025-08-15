from core.common.abstract_repository import GetModel
from ..domain.item import ServiceItem, ProductItem
from ..domain.order import Order
from .dto import FilterOrderDto, FilterServiceItemByDto, EmployeeCalendarDto
from abc import ABC, abstractmethod
from typing import List, Tuple
from datetime import date
from decimal import Decimal

class GetServiceItem(GetModel[ServiceItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ServiceItem]: ...
    
    @abstractmethod
    def filter_service_items(self, filter_dto: FilterServiceItemByDto) -> Tuple[List[ServiceItem], int]: ...
    
    @abstractmethod
    def get_employee_total_facturado(self, employee_id: str, start_date: date, end_date: date) -> Decimal: ...
    
    @abstractmethod
    def get_employee_total_pagado(self, employee_id: str, start_date: date, end_date: date) -> Decimal: ...

    @abstractmethod
    def get_employee_calendar(self, employee_id: str) -> List[EmployeeCalendarDto]: ...


class GetProductItem(GetModel[ProductItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ProductItem]: ...


class GetOrder(GetModel[Order], ABC):
    @abstractmethod
    def filter_orders(self, dto: FilterOrderDto) -> Tuple[List[Order], int]: ...
