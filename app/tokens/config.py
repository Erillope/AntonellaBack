from .repository import DjangoSaveToken, DjangoDeleteToken, DjangoGetToken
from core.token import TokenService

class TokenServiceConfig:
    token_service = TokenService(get_token=DjangoGetToken())
    save_token = DjangoSaveToken()
    delete_token = DjangoDeleteToken()