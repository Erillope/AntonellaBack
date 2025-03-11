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


class AlreadyExistsSuperAdminException(AuthServiceException):
    @classmethod
    def already_exists(cls) -> 'AlreadyExistsSuperAdminException':
        return cls('Ya existe un super administrador')