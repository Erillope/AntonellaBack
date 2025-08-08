from pydantic import BaseModel, model_validator
from typing import Optional
from decimal import Decimal
from .values import OrderStatusInfo
from core.common.values import ID
from .events import OrderSaved, OrderDeleted
from datetime import date, datetime
from core.common.config import AppConfig

class Order(BaseModel):
    id: str
    client_id: str
    status: OrderStatusInfo
    card_charge: Decimal
    iva: Decimal
    created_date: date
    order_date: Optional[datetime]
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Order':
        '''Valida los datos del pedido'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        ID.validate(self.client_id)
    
    def update_data(self, client_id: Optional[str] = None, status: Optional[OrderStatusInfo] = None) -> None:
        if client_id is not None:
            ID.validate(client_id)
            self.client_id = client_id
        if status is not None:
            self.status = status
        self._validate_data()
    
    def save(self) -> None:
        OrderSaved(self).publish()
        
    def delete(self) -> None:
        OrderDeleted(self.id).publish()


class OrderFactory:
    @classmethod
    def create(cls, client_id: str, status: OrderStatusInfo) -> Order:
        return Order(
            id=ID.generate(),
            client_id=client_id,
            card_charge=Decimal('1'),
            status=status,
            created_date=date.today(),
            order_date=None,
            iva=AppConfig.iva()
        )
    
    @classmethod
    def load(cls, id: str, client_id: str, status: OrderStatusInfo, card_charge: Decimal, created_date: date, 
             order_date: Optional[datetime], iva: Decimal) -> Order:
        return Order(
            id=id,
            client_id=client_id,
            card_charge=card_charge,
            status=status,
            created_date=created_date,
            order_date=order_date,
            iva=iva
        )