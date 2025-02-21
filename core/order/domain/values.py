from pydantic import BaseModel, model_validator
from enum import Enum
from decimal import Decimal
from core.common.values import AmountValue, ID
from core.common.exceptions import InvalidTimeRange
from datetime import date, time
from core.common.config import AppConfig

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
        AmountValue.validate(self.base_price)
        AmountValue.validate(self.sale_price)
        AmountValue.validate(self.iva)
        AmountValue.validate(self.card_charge)
        pass
    
    @classmethod
    def calculate(cls, base_price: Decimal) -> 'Price':
        cls._validate_data()
        cls.sale_price = base_price + AppConfig.iva() + cls.card_charge
        return cls

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
        ID.validate(self.employee_id)
        AmountValue.validate(self.percentage)
        AmountValue.validate(self.amount)
        pass
    
    @classmethod
    def calculate(cls, employee_id: str, percentage: Decimal) -> 'Payment':
        cls._validate_data()
        cls.amount = Price.base_price * percentage
        return cls


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
        if(self.end_time < self.start_time):
            raise InvalidTimeRange.invalid_range(self.start_time, self.end_time)
        
        if(self.day < date.today().day):
            raise Exception("Dia Incorrecto")
        
        pass