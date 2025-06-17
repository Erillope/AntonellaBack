from decimal import Decimal
from pydantic import BaseModel
from ..domain.values import Progresstatus, OrderStatusInfo, DateInfo
from typing import Optional, List
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

class UpdateServiceItemDto(BaseModel):
    id: str
    service_id: Optional[str] = None
    payment_percentage: Optional[Decimal] = None
    date_info: Optional[DateInfo] = None
    status: Optional[Progresstatus] = None
    base_price: Optional[Decimal] = None
    payments: List[PaymentDto] = []


class CreateOrderDto(BaseModel):
    client_id: str
    status: OrderStatusInfo


class UpdateOrderDto(BaseModel):
    id: str
    client_id: Optional[str] = None
    status: Optional[OrderStatusInfo] = None
    

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


class UpdateProductItemDto(BaseModel):
    id: str
    product_id: Optional[str] = None
    quantity: Optional[int] = None
    base_price: Optional[Decimal] = None