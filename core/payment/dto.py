from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum

class DebitRequestDto(BaseModel):
    order_id: str
    taxable_amount: Decimal
    card_id: str

class DebitResponseDto(BaseModel):
    transaction_id: str
    ok: bool
    order_id: str
    amount: Decimal
    taxable_amount: Decimal
    tax_percentage: Decimal
    user_id: str
    card_id: str
    created_at: datetime


class CardType(str, Enum):
    VI = "vi"
    MC = "mc"
    AX = "ax"
    DI = "di"
    DC = "dc"
    MS = "ms"
    CS = "cs"
    SO = "so"
    UP = "up"


class AddUserCardDto(BaseModel):
    user_id: str
    number: str
    expiry_month: int
    expiry_year: int
    cvc: str


class AddUserCardWithCardIdDto(BaseModel):
    user_id: str
    card_id: str
    number: str
    type: CardType = CardType.VI


class UserCardDto(BaseModel):
    user_id: str
    card_id: str
    number: str
    type: CardType = CardType.VI