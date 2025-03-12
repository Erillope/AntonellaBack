from core.user.domain.exceptions import UserException

class AuthServiceException(UserException): ...

class IncorrectPasswordException(AuthServiceException):
    @classmethod
    def incorrect_password(cls) -> 'IncorrectPasswordException':
        return cls('Contraseña incorrecta')


class AlreadyExistsSuperAdminException(AuthServiceException):
    @classmethod
    def already_exists(cls) -> 'AlreadyExistsSuperAdminException':
        return cls('Ya existe un super administrador')