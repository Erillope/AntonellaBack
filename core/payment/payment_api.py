from abc import ABC, abstractmethod
from .dto import DebitRequestDto, DebitResponseDto, AddUserCardDto

class PaymentAPI(ABC):
    @abstractmethod
    def add_user_card(self, dto: AddUserCardDto) -> None: ...

    @abstractmethod
    def debit(self, dto: DebitRequestDto) -> DebitResponseDto: ...