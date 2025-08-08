from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class DebitRequestDto(BaseModel):
    order_id: str
    taxable_amount: Decimal
    user_id: str

class DebitResponseDto(BaseModel):
    transaction_id: str
    ok: bool
    order_id: str
    amount: Decimal
    taxable_amount: Decimal
    tax_percentage: Decimal
    user_id: str
    created_at: datetime


class AddUserCardDto(BaseModel):
    user_id: str
    number: str
    expiry_month: int
    expiry_year: int
    cvc: str


class AddUserCardWithCardIdDto(BaseModel):
    user_id: str
    card_id: str