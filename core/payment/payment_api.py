from abc import ABC, abstractmethod
from .dto import DebitRequestDto, DebitResponseDto

class PaymentAPI(ABC):
    @abstractmethod
    def debit(self, dto: DebitRequestDto) -> DebitResponseDto: ...