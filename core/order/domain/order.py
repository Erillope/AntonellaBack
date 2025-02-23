from pydantic import BaseModel, model_validator
from typing import List
from decimal import Decimal
from .item import ServiceItem
from .values import OrderStatusInfo, Price
from core.common.values import ID

class Order(BaseModel):
    id: str
    client_id: str
    service_items: List[ServiceItem]
    status: OrderStatusInfo
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Order':
        '''Valida los datos del pedido'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        ID.validate(self.client_id)
    
    def total_payment(self) -> Decimal:
        return Decimal(0)
    
    def profits(self) -> Decimal:
        return Decimal(0)
    
    def add_service_item(self) -> None:
        pass
    
    def remove_service_item(self) -> None:
        pass
    
    def total_price(self) -> Price:
        price: Price
        return price
    