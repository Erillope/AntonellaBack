from pydantic import BaseModel, model_validator
from decimal import Decimal
from datetime import date, time
from .values import Progresstatus, Price, Payment, DateInfo
from typing import List
from core.common.values import ID, AmountValue
from .exceptions import EmployeeAlreadyIsInServiceItem
from functools import reduce

class ServiceItem(BaseModel):
    id: str
    service_id: str
    order_id: str
    payment_percentage: Decimal
    date_info: DateInfo
    status: Progresstatus
    price: Price
    payments: List[Payment]
    created_date: date
    
    @model_validator(mode='after')
    def validate_data(self) -> 'ServiceItem':
        '''Valida los datos del item de servicio'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        ID.validate(self.service_id)
        ID.validate(self.order_id)
        AmountValue.validate_percentage(self.payment_percentage)
        self.date_info._validate_data()
        self.price._validate_data()
    
    def total_payment(self) -> Decimal:
        return reduce(lambda x, y: x + y.amount, self.payments, Decimal(0))
    
    def profits(self) -> Decimal:
        return self.price.base_price - self.total_payment()
    
    def add_employee_payment(self, employee_id: str) -> None:
        payment = Payment.calculate(employee_id, self.price.base_price, self.payment_percentage)
        if payment in self.payments:
            raise EmployeeAlreadyIsInServiceItem.already_in_service_item(employee_id)
        self.payments.append(payment)
    
    def remove_employee_payment(self, employee_id: str) -> None:
        for payment in self.payments:
            if payment.employee_id == employee_id:
                self.payments.remove(payment)
                break


class ServiceItemFactory:
    @classmethod
    def create(cls, service_id: str, order_id: str, payment_percentage: Decimal, day: date, start_time: time,
               end_time: time) -> ServiceItem:
       service_item: ServiceItem
       return service_item
   
    @classmethod
    def load(cls, id: str, service_id: str, order_id: str, payment_percentage: Decimal, day: DateInfo, 
            status: Progresstatus, price: Price, payments: List[Payment], created_date: date) -> ServiceItem:
        service_item: ServiceItem
        return service_item