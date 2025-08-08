from abc import ABC, abstractmethod
from .dto import DebitRequestDto, DebitResponseDto, AddUserCardDto, UserCardDto
from typing import List

class PaymentAPI(ABC):
    @abstractmethod
    def list_user_cards(self, user_id: str) -> List[UserCardDto]: ...

    @abstractmethod
    def add_user_card(self, dto: AddUserCardDto) -> UserCardDto: ...

    @abstractmethod
    def debit(self, dto: DebitRequestDto) -> DebitResponseDto: ...