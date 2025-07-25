from core.common.abstract_repository import GetModel
from ..domain.item import ServiceItem, ProductItem
from ..domain.order import Order
from .dto import FilterOrderDto
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import date
from decimal import Decimal

class GetServiceItem(GetModel[ServiceItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ServiceItem]: ...
    
    @abstractmethod
    def prepare_client_id_filter(self, client_id: str) -> None: ...
    
    @abstractmethod
    def prepare_start_date_filter(self, start_date: date) -> None: ...
    
    @abstractmethod
    def prepare_end_date_filter(self, end_date: date) -> None: ...
    
    @abstractmethod
    def prepare_status_filter(self, status: str) -> None: ...
    
    @abstractmethod
    def prepare_service_id_filter(self, service_id: str) -> None: ...
    
    @abstractmethod
    def prepare_employee_id_filter(self, employee_id: str) -> None: ...
    
    @abstractmethod
    def get_filtered_service_items(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ServiceItem]: ...
    
    @abstractmethod
    def get_employee_total_facturado(self, employee_id: str, start_date: date, end_date: date) -> Decimal: ...
    
    @abstractmethod
    def get_employee_total_pagado(self, employee_id: str, start_date: date, end_date: date) -> Decimal: ...


class GetProductItem(GetModel[ProductItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ProductItem]: ...


class GetOrder(GetModel[Order], ABC):
    @abstractmethod
    def filter_orders(self, dto: FilterOrderDto) -> Tuple[List[Order], int]: ...