from core.user.domain.exceptions import UserException

class AuthServiceException(UserException): ...

class IncorrectPasswordException(AuthServiceException):
    @classmethod
    def incorrect_password(cls) -> 'IncorrectPasswordException':
        return cls('Contraseña incorrecta')