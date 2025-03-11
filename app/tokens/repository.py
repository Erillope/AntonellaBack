from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.token.tokens import Token, CreatedToken, DeletedToken
from .models import TokenTableData
from .mapper import TokenTableMapper
from core.common.events import Event, EventSubscriber

class DjangoGetToken(DjangoGetModel[TokenTableData, Token]):
    def __init__(self) -> None:
        super().__init__(TokenTableData, TokenTableMapper())


class DjangoSaveToken(DjangoSaveModel[TokenTableData, Token], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(TokenTableMapper())
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, CreatedToken):
            self.save(event.token)


class DjangoDeleteToken(DjangoDeleteModel[TokenTableData, Token], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(TokenTableData, TokenTableMapper(), DjangoGetToken())
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, DeletedToken):
            self.delete(event.token_id)