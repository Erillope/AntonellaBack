from core.payment.payment_api import PaymentAPI
from core.payment.dto import DebitRequestDto, DebitResponseDto
import time
import hashlib
from base64 import b64encode
import requests # type: ignore
from typing import Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from app.payment.models import UserCard, DebitPayment
from core.common.config import AppConfig

class PaymentezApi(PaymentAPI):
    def __init__(self, api_key: str, secret_key: str) -> None:
        self.auth_token = self._generate_auth_token(api_key, secret_key)
        self.url = 'https://ccapi-stg.paymentez.com/v2/'
        self.headers = {
            'Auth-Token': self.auth_token,
            'Content-Type': 'application/json'
        }
    
    def add_user_card(self, card_id: str, user_id: str) -> None:
        card = UserCard.objects.create(id=card_id, user_id=user_id)
        card.save()
        
    def debit(self, dto: DebitRequestDto) -> DebitResponseDto:
        response = self._do_request(dto)
        data = self._response_data(response['transaction'], dto)
        DebitPayment.save_payment(data)
        return data
    
    def _do_request(self, dto: DebitRequestDto) -> Dict[str, Any]:
        response = requests.post(
            self.url + 'transaction/debit/',
            headers=self.headers,
            json=self._json_data(dto),
        )
        if response.status_code != 200:
            raise Exception(f"Ocurrió un error al procesar el pago")
        data: Dict[str, Any] = response.json()
        return data
    
    def _response_data(self, data: Dict[str, Any], dto: DebitRequestDto) -> DebitResponseDto:
        return DebitResponseDto(
            transaction_id = data['id'],
            ok = data['status'] == 'success',
            order_id = dto.order_id,
            taxable_amount = dto.taxable_amount,
            tax_percentage = AppConfig.iva(),
            amount = data['amount'],
            user_id = dto.user_id,
            created_at = datetime.fromisoformat(data['payment_date'])
        )
        
    def _json_data(self, dto: DebitRequestDto) -> Dict[str, Any]:
        card = UserCard.objects.get(user__id=dto.user_id)
        return {
            'order': self._order_data(dto),
            'user': {
                'id': dto.user_id,
                'email': card.user.email,
            },
            'card': {
                'token': card.id,
            }
        }
        
    def _order_data(self, dto: DebitRequestDto) -> Dict[str, Any]:
        vat = (dto.taxable_amount * (AppConfig.iva() / Decimal(100))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        amount = dto.taxable_amount + vat
        return {
            'amount': float(amount),
            'description': 'Order transaction',
            'dev_reference': dto.order_id,
            'taxable_amount': float(dto.taxable_amount),
            'tax_percentage': float(AppConfig.iva()),
            'vat': float(vat),
        }
    
    def _generate_auth_token(self, api_key: str, secret_key: str) -> str:
        unix_timestamp = str(int(time.time()))
        uniq_token_string = secret_key + unix_timestamp
        uniq_token_hash = hashlib.sha256(uniq_token_string.encode('utf-8')).hexdigest()
        token_string = f'{api_key};{unix_timestamp};{uniq_token_hash}'
        auth_token = b64encode(token_string.encode('utf-8')).decode('utf-8')
        return auth_token