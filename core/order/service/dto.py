from decimal import Decimal
from pydantic import BaseModel
from ..domain.values import Progresstatus, OrderStatusInfo, DateInfo, PaymentStatus, PaymentType, OrderStatus
from typing import Optional, List, Tuple
from datetime import date, time


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
    discount: Optional[Decimal] = None

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


class UpdateOrderDto(BaseModel):
    id: str
    client_id: Optional[str] = None
    status: Optional[OrderStatus] = None
    progress_status: Optional[Progresstatus] = None
    payment_status: Optional[PaymentStatus] = None
    payment_type: Optional[PaymentType] = None
    client_confirmed: Optional[OrderStatus] = None
    

class OrderDto(BaseModel):
    id: str
    client_id: str
    status: OrderStatusInfo
    created_date: date


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


class ProductItemDto(BaseModel):
    id: Optional[str] = None
    order_id: str
    product_id: str
    quantity: int
    base_price: Decimal
    discount: Optional[Decimal] = None


class UpdateProductItemDto(BaseModel):
    id: str
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    base_price: Optional[Decimal] = None


class FilterServiceItemByDto(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    client_id: Optional[str] = None
    status: Optional[Progresstatus] = None
    service_id: Optional[str] = None
    employee_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class RequestEmployeeServiceInfoDto(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    limit: Optional[int] = None
    offset: Optional[int] = None
    
class EmployeeServiceInfoDto(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    total_facturado: Decimal
    total_pagado: Decimal
    service_items: List[ServiceItemDto]