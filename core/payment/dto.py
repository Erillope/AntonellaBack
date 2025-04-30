from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

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