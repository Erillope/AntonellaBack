from decimal import Decimal
from pydantic import BaseModel
from ..domain.values import Progresstatus, OrderStatusInfo, DateInfo
from typing import Optional, List
from datetime import date, time


class PaymentDto(BaseModel):
    employee_id: str
    percentage: Optional[Decimal] = None


class ServiceItemDto(BaseModel):
    order_id: str
    service_id: str
    payment_percentage: Optional[Decimal] = None
    date_info: DateInfo
    status: Optional[Progresstatus] = None
    base_price: Decimal
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