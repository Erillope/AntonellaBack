from pydantic import BaseModel, model_validator
from decimal import Decimal
from datetime import date, time
from .values import Progresstatus, Price, Payment, DateInfo
from typing import List
from core.common.config import AppConfig
from core.common.values import ID, AmountValue

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
        AmountValue.validate(self.payment_percentage)
        self.date_info._validate_data()
        self.price._validate_data()
        pass
    
    def total_payment(self) -> Decimal:
        return Decimal(0)
    
    def profits(self) -> Decimal:
        return Decimal(0)
    
    def add_employee(self) -> None:
        
        pass
    
    def remove_employee(self) -> None:
        pass