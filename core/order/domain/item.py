from pydantic import BaseModel, model_validator, PrivateAttr
from decimal import Decimal
from datetime import date, time
from .values import Progresstatus, Price, Payment, DateInfo
from typing import List
from core.common.values import ID, AmountValue
from .exceptions import EmployeeAlreadyIsInServiceItem, MissingPaymentPercentageException, MissingOrderIdException
from typing import Optional
from .events import ServiceItemSaved, ServiceItemDeleted

class ServiceItem(BaseModel):
    id: str
    service_id: str
    payment_percentage: Optional[Decimal] = None
    date_info: DateInfo
    status: Progresstatus
    price: Optional[Price] = None
    payments: List[Payment]
    _order_id: str = PrivateAttr("")
    
    @model_validator(mode='after')
    def validate_data(self) -> 'ServiceItem':
        '''Valida los datos del item de servicio'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        ID.validate(self.service_id)
        if self.payment_percentage:
            AmountValue.validate_percentage(self.payment_percentage)
        self.date_info._validate_data()
        self.price._validate_data() if self.price else None
    
    def update_data(self, service_id: Optional[str] = None, payment_percentage: Optional[Decimal] = None,
                        date_info: Optional[DateInfo] = None, status: Optional[Progresstatus] = None,
                        base_price: Optional[Decimal] = None, payments: Optional[List[Payment]] = None) -> None:
        if service_id is not None:
            ID.validate(service_id)
            self.service_id = service_id
        if payment_percentage is not None:
            AmountValue.validate_percentage(payment_percentage)
            self.payment_percentage = payment_percentage
        if date_info is not None:
            date_info._validate_data()
            self.date_info = date_info
        if status is not None:
            self.status = status
        if base_price is not None:
            self.price = Price.calculate(base_price)
        if payments is not None:
            self.payments = payments
        self._validate_data()
    
    def remove_employee_payment(self, employee_id: str) -> None:
        for payment in self.payments:
            if payment.employee_id == employee_id:
                self.payments.remove(payment)
                break
    
    def set_order_id(self, order_id: str) -> None:
        ID.validate(order_id)
        self._order_id = order_id
    
    def set_payment_percentage(self, payment_percentage: Decimal) -> None:
        AmountValue.validate_percentage(payment_percentage)
        self.payment_percentage = payment_percentage
    
    def get_order_id(self) -> str:
        if not self._order_id:
            raise MissingOrderIdException.missing_order_id()
        return self._order_id
    
    def save(self) -> None:
        if not self._order_id: raise MissingOrderIdException.missing_order_id()
        ServiceItemSaved(self).publish()
    
    def delete(self) -> None:
        ServiceItemDeleted(self.id).publish()

class ServiceItemFactory:
    @classmethod
    def create(cls, service_id: str, day: date, start_time: time, base_price: Optional[Decimal], payments: List[Payment]) -> ServiceItem:
        return ServiceItem(
            id= ID.generate(),
            service_id= service_id,
            date_info= DateInfo(day= day, start_time= start_time),
            status= Progresstatus.PENDING,
            price= Price.calculate(base_price) if base_price else None,
            payments= payments,
        )
    
    @classmethod
    def load(cls, id: str, service_id: str, order_id: str, day: DateInfo, status: Progresstatus,
             price: Optional[Price], payments: List[Payment],
             payment_percentage: Optional[Decimal] = None) -> ServiceItem:
        item = ServiceItem(
            id= id,
            service_id= service_id,
            payment_percentage= payment_percentage,
            date_info= day,
            status= status,
            price= price,
            payments= payments,
        )
        item.set_order_id(order_id)
        return item