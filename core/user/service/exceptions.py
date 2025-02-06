from core.user.domain.exceptions import UserException

class AuthServiceException(UserException): ...

class IncorrectPasswordException(AuthServiceException):
    @classmethod
    def incorrect_password(cls) -> 'IncorrectPasswordException':
        return cls('Contraseña incorrecta')


class AlreadyExistsRoleException(AuthServiceException):
    @classmethod
    def already_exists(cls, rolename: str) -> 'AlreadyExistsRoleException':
        return cls(f'El rol {rolename} ya existe')


class AlreadyExistsUserException(AuthServiceException):
    @classmethod
    def already_exists(cls, username: str) -> 'AlreadyExistsUserException':
        return cls(f'El usuario {username} ya existe')