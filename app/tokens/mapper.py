from app.common.table_mapper import TableMapper
from .models import TokenTableData
from core.token import Token
from django.utils import timezone

class TokenTableMapper(TableMapper[TokenTableData, Token]):
    def to_model(self, token_table: TokenTableData) -> Token:
        return Token(
            id=str(token_table.id),
            user_id=str(token_table.user_id),
            created_at=timezone.localtime(token_table.created_at),
            expired_at=timezone.localtime(token_table.expired_at)
        )
    
    def to_table(self, token: Token) -> TokenTableData:
        return TokenTableData(
            id=token.id,
            user_id=token.user_id,
            created_at=token.created_at,
            expired_at=token.expired_at
        )
