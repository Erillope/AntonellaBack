from pydantic import BaseModel, model_validator
from enum import Enum
from decimal import Decimal
from core.common.values import AmountValue, ID
from core.common.exceptions import InvalidTimeRange
from datetime import date, time
from core.common.config import AppConfig
from typing import Optional

class Progresstatus(str, Enum):
    '''Estados de un item de servicio'''
    PENDING = 'PENDIENTE'
    IN_PROGRESS = 'EN_PROGRESO'
    FINISHED = 'FINALIZADO'

    
class OrderStatus(str, Enum):
    '''Estados de un pedido'''
    CONFIRMED = 'CONFIRMADO'
    NOT_CONFIRMED = 'NO_CONFIRMADO'


class PaymentStatus(str, Enum):
    '''Estados de un pago'''
    PENDING = 'PENDIENTE'
    PAID = 'PAGADO'


class PaymentType(str, Enum):
    '''Tipos de pago'''
    CASH = 'EFECTIVO'
    CARD = 'TARJETA'

class OrderStatusInfo(BaseModel):
    '''Información de estado de un pedido'''
    status: OrderStatus
    progress_status: Progresstatus
    payment_status: PaymentStatus
    payment_type: PaymentType

    
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
        AmountValue.validate(self.base_price)
        AmountValue.validate(self.sale_price)
        AmountValue.validate(self.iva)
        AmountValue.validate(self.card_charge)
    
    @classmethod
    def calculate(cls, base_price: Decimal, card_charge: Decimal = Decimal(0)) -> 'Price':
        sale_price = base_price*(1+AppConfig.iva()) + card_charge
        return cls(base_price=base_price, sale_price=sale_price,
                   iva=AppConfig.iva(), card_charge=card_charge)

class Payment(BaseModel):
    employee_id: str
    percentage: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Payment':
        '''Valida los datos del pago'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.employee_id)
        if not self.percentage or not self.amount: return
        AmountValue.validate(self.percentage)
        AmountValue.validate(self.amount)
    
    @classmethod
    def calculate(cls, employee_id: str, base_price: Decimal, percentage: Decimal) -> 'Payment':
        amount = base_price * percentage
        return cls(employee_id=employee_id, percentage=percentage, amount=amount)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Payment):
            return self.employee_id == value.employee_id
        return False


class DateInfo(BaseModel):
    '''Información de fecha'''
    day: date
    start_time: time
    end_time: Optional[time] = None

    @model_validator(mode='after')
    def validate_data(self) -> 'DateInfo':
        '''Valida los datos de la fecha'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        if not self.end_time: return
        if not self._is_in_time_range():
            raise InvalidTimeRange.invalid_range(self.start_time, self.end_time)
        if(self.end_time < self.start_time):
            raise InvalidTimeRange.invalid_range(self.start_time, self.end_time)
    
    def _is_in_time_range(self) -> bool:
        if not self.end_time: return True
        is_valid_start = AppConfig.start_time() < self.start_time < AppConfig.end_time()
        is_valid_end = AppConfig.start_time() < self.end_time < AppConfig.end_time()
        return is_valid_start and is_valid_end