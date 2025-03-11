from core.common import SystemException

class TokenException(SystemException): ...


class InvalidTokenException(TokenException):
    @classmethod
    def invalid(cls, token: str) -> 'InvalidTokenException':
        return cls(f'El token {token} no existe o está caducado')