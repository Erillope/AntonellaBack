from decimal import Decimal
from pydantic import BaseModel
from ..domain.values import Progresstatus, OrderStatusInfo, DateInfo, PaymentStatus, PaymentType, OrderStatus
from typing import Optional, List
from datetime import date, time, datetime
from core.store_service.domain.values import ServiceType

class PaymentDto(BaseModel):
    employee_id: str
    percentage: Optional[Decimal] = None


class ServiceItemDto(BaseModel):
    id: Optional[str] = None
    order_id: str
    service_id: str
    payment_percentage: Optional[Decimal] = None
    date_info: DateInfo
    status: Optional[Progresstatus] = None
    base_price: Optional[Decimal] = None
    payments: List[PaymentDto]

class UpdateServiceItemDto(BaseModel):
    id: str
    service_id: Optional[str] = None
    payment_percentage: Optional[Decimal] = None
    date_info: Optional[DateInfo] = None
    status: Optional[Progresstatus] = None
    base_price: Optional[Decimal] = None
    payments: Optional[List[PaymentDto]] = None


class CreateOrderDto(BaseModel):
    client_id: str
    status: OrderStatusInfo
    iva: Optional[bool] = None


class UpdateOrderDto(BaseModel):
    id: str
    client_id: Optional[str] = None
    status: Optional[OrderStatus] = None
    progress_status: Optional[Progresstatus] = None
    payment_status: Optional[PaymentStatus] = None
    payment_type: Optional[PaymentType] = None
    client_confirmed: Optional[OrderStatus] = None
    iva: Optional[Decimal] = None


class OrderDto(BaseModel):
    id: str
    client_id: str
    status: OrderStatusInfo
    created_date: datetime
    order_date: Optional[datetime] = None
    card_charge: Decimal
    iva: Decimal

class FilterOrderResponseDto(BaseModel):
    orders: List[OrderDto]
    total_count: int
    filtered_count: int

class RequestEmployeeScheduleDto(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    
    
class EmployeeScheduleDto(BaseModel):
    employee_id: str
    schedule: List['EmployeeScheduleItemDto']
    
    class EmployeeScheduleItemDto(BaseModel):
        service_id: str
        start_time: time
        end_time: time

class EmployeeCalendarDto(BaseModel):
    day: date
    start_time: time
    end_time: time

class ProductItemDto(BaseModel):
    id: Optional[str] = None
    order_id: str
    product_id: str
    quantity: int
    base_price: Decimal


class UpdateProductItemDto(BaseModel):
    id: str
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    base_price: Optional[Decimal] = None


class FilterServiceItemByDto(BaseModel):
    only_count: Optional[bool] = False
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    client_id: Optional[str] = None
    status: Optional[Progresstatus] = None
    service_id: Optional[str] = None
    employee_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

class FilterServiceItemResponseDto(BaseModel):
    service_items: List[ServiceItemDto]
    only_count: Optional[bool] = False
    total_count: int
    filtered_count: int


class RequestEmployeeServiceInfoDto(BaseModel):
    employee_id: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    
class EmployeeServiceInfoDto(BaseModel):
    employee_id: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_facturado: Decimal
    total_pagado: Decimal
    service_items: List[ServiceItemDto]

class FilterOrderDto(BaseModel):
    client_name: Optional[str] = None
    client_id: Optional[str] = None
    status: Optional[OrderStatus] = None
    progress_status: Optional[Progresstatus] = None
    service_type: Optional[ServiceType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    only_count: Optional[bool] = False