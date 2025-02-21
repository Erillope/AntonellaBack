from pydantic import BaseModel, model_validator
from enum import Enum
from decimal import Decimal
from core.common.values import AmountValue
from core.common.exceptions import InvalidTimeRange
from datetime import date, time

class Progresstatus(str, Enum):
    '''Estados de un item de servicio'''
    PENDING = 'PENDIENTE'
    IN_PROGRESS = 'EN PROGRESO'
    FINISHED = 'FINALIZADO'

    
class OrderStatus(str, Enum):
    '''Estados de un pedido'''
    CONFIRMED = 'CONFIRMADO'
    NOT_CONFIRMED = 'NO CONFIRMADO'


class PaymentStatus(str, Enum):
    '''Estados de un pago'''
    PENDING = 'PENDIENTE'
    PAID = 'PAGADO'


class PayementType(str, Enum):
    '''Tipos de pago'''
    CASH = 'EFECTIVO'
    CARD = 'TARJETA'

class OrderStatusInfo(BaseModel):
    '''Información de estado de un pedido'''
    status: OrderStatus
    progress_status: Progresstatus
    payment_status: PaymentStatus
    payment_type: PayementType

    
class Price(BaseModel):
    '''Precio de un item de servicio'''
    base_price: Decimal
    sale_price: Decimal
    iva: Decimal
    card_charge: Decimal
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Price':
        '''Valida los datos del precio'''
        self._validate_data()
        return self

    def _validate_data(self) -> None:
        pass
    
    @classmethod
    def calculate(cls, base_price: Decimal) -> 'Price':
        price: Price
        return price


class Payment(BaseModel):
    employee_id: str
    percentage: Decimal
    amount: Decimal
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Payment':
        '''Valida los datos del pago'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        pass
    
    @classmethod
    def calculate(cls, emplotee_id: str, percentage: Decimal) -> 'Payment':
        payment: Payment
        return payment


class DateInfo(BaseModel):
    '''Información de fecha'''
    day: date
    start_time: time
    end_time: time

    @model_validator(mode='after')
    def validate_data(self) -> 'DateInfo':
        '''Valida los datos de la fecha'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        pass