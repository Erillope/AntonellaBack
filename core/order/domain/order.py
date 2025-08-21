from pydantic import BaseModel, model_validator
from typing import Optional
from decimal import Decimal
from .values import OrderStatusInfo, Progresstatus
from core.common.values import ID, GuayaquilDatetime
from .events import OrderSaved, OrderDeleted
from datetime import datetime
from core.common.config import AppConfig

class Order(BaseModel):
    id: str
    client_id: str
    status: OrderStatusInfo
    card_charge: Decimal
    iva: Decimal
    created_date: datetime
    order_date: Optional[datetime]
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Order':
        '''Valida los datos del pedido'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        ID.validate(self.client_id)

    def update_data(self, client_id: Optional[str] = None, status: Optional[OrderStatusInfo] = None, iva: Optional[Decimal] = None) -> None:
        if client_id is not None:
            ID.validate(client_id)
            self.client_id = client_id
        if status is not None:
            self.status = status
        if iva is not None:
            self.iva = iva
        self._validate_data()
    
    def save(self) -> None:
        OrderSaved(self).publish()
        
    def delete(self) -> None:
        OrderDeleted(self.id).publish()


class OrderFactory:
    @classmethod
    def create(cls, client_id: str, status: OrderStatusInfo, iva: Optional[bool] = None) -> Order:
        return Order(
            id=ID.generate(),
            client_id=client_id,
            card_charge=Decimal('0'),
            status=OrderStatusInfo(
                status=status.status,
                progress_status=Progresstatus.PENDING,
                payment_status=status.payment_status,
                payment_type=status.payment_type,
                client_confirmed=status.client_confirmed
            ),
            created_date=GuayaquilDatetime.now(),
            order_date=None,
            iva=AppConfig.iva() if iva else Decimal('0')
        )
    
    @classmethod
    def load(cls, id: str, client_id: str, status: OrderStatusInfo, card_charge: Decimal, created_date: datetime, 
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