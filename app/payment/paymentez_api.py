from core.payment.payment_api import PaymentAPI
from core.payment.dto import DebitRequestDto, DebitResponseDto
import time
import hashlib
from base64 import b64encode
import requests # type: ignore
from typing import Dict, Any, List
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from app.payment.models import UserCard, DebitPayment
from core.common.config import AppConfig
from core.payment.dto import AddUserCardDto, AddUserCardWithCardIdDto, UserCardDto, CardType
from app.user.models import UserAccountTableData
from core.common import SystemException, GuayaquilDatetime
from typing import Optional

class PaymentException(SystemException):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class AlreadyRegisteredCardException(SystemException):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class CardNotValidException(SystemException):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class CardNotFoundException(SystemException):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class PaymentezApi(PaymentAPI):
    def __init__(self, api_key: str, secret_key: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = 'https://ccapi-stg.paymentez.com/v2/'


    def add_user_card(self, dto: AddUserCardDto) -> UserCardDto:
        response = self._do_add_card_request(dto)
        data: Dict[str, Any] = response['card']
        self._save_user_card(dto.user_id, data['token'], data['number'], CardType(data['type']))
        return UserCardDto(
            user_id=dto.user_id,
            card_id=data['token'],
            number=data['number'],
            type=data.get('type', None)
        )

    def list_user_cards(self, user_id: str) -> List[UserCardDto]:
        user_cards = UserCard.objects.filter(user__id=user_id)
        return [UserCardDto(
            user_id=str(card.user.id),
            card_id=card.card_id,
            number=card.number,
            type=card.type
        ) for card in user_cards]
    
    def add_user_card_with_card_id(self, dto: AddUserCardWithCardIdDto) -> None:
        self._save_user_card(dto.user_id, dto.card_id, dto.number, dto.type)

    def _save_user_card(self, user_id: str, card_id: str, number: str, type: Optional[CardType]) -> UserCard:
        card_type : str
        if type:
            card_type = type.value
        card: UserCard = UserCard.objects.create(card_id=card_id, user_id=user_id, number=number, type=card_type)
        return card

    def debit(self, dto: DebitRequestDto) -> DebitResponseDto:
        response = self._do_request(dto)
        data = self._response_data(response['transaction'], dto)
        DebitPayment.save_payment(data)
        return data
    
    def _do_request(self, dto: DebitRequestDto) -> Dict[str, Any]:
        response = requests.post(
            self.url + 'transaction/debit/',
            headers=self._generate_headers(),
            json=self._json_data(dto),
        )
        if response.status_code != 200:
            raise PaymentException(f"Ocurrió un error al procesar el pago")
        data: Dict[str, Any] = response.json()
        return data
    
    def _do_add_card_request(self, dto: AddUserCardDto) -> Dict[str, Any]:
        user = UserAccountTableData.objects.get(id=dto.user_id)
        response = requests.post(
            self.url + 'card/add/',
            headers=self._generate_headers(),
            json={
                "user": {
                    "id": dto.user_id,
                    "email": user.email,
                },
                "card": {
                    "number": dto.number,
                    "expiry_month": dto.expiry_month,
                    "expiry_year": dto.expiry_year,
                    "cvc": dto.cvc,
                }
            },
        )
        if response.status_code != 200:
            error_data: str = response.json()['error']['type']
            if "already" in error_data:
                raise AlreadyRegisteredCardException(f"La tarjeta ya está registrada")
            print(f"Error al procesar la tarjeta: {response.json()}")
            raise PaymentException(f"Ocurrió un error al procesar la tarjeta")
        data: Dict[str, Any] = response.json()
        if data['card']['status'] != 'valid':
            raise CardNotValidException(f"La tarjeta no es válida")
        return data
    
    def _response_data(self, data: Dict[str, Any], dto: DebitRequestDto) -> DebitResponseDto:
        card = UserCard.objects.get(card_id=dto.card_id)
        return DebitResponseDto(
            transaction_id = data['id'],
            ok = data['status'] == 'success',
            order_id = dto.order_id,
            taxable_amount = dto.taxable_amount,
            tax_percentage = AppConfig.iva(),
            amount = data['amount'],
            user_id = str(card.user.id),
            card_id = card.card_id,
            created_at = GuayaquilDatetime.localize(datetime.fromisoformat(data['payment_date']))
        )
        
    def _json_data(self, dto: DebitRequestDto) -> Dict[str, Any]:
        if not UserCard.objects.filter(card_id=dto.card_id).exists():
            raise CardNotFoundException(f"La tarjeta no fue encontrada")
        card = UserCard.objects.get(card_id=dto.card_id)
        return {
            'order': self._order_data(dto),
            'user': {
                'id': str(card.user.id),
                'email': card.user.email,
            },
            'card': {
                'token': card.card_id,
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
    
    def _generate_headers(self) -> Dict[str, str]:
        return {
            'Auth-Token': self._generate_auth_token(self.api_key, self.secret_key),
            'Content-Type': 'application/json'
        }