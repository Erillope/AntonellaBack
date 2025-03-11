from core.common import SystemException
from datetime import date

class UserException(SystemException): ...

class InvalidUserPasswordException(UserException):
    @classmethod
    def invalid_password(cls, password: str) -> "InvalidUserPasswordException":
        return cls(f"La contraseña '{password}' es inválida")


class InvalidUserNameException(UserException):
    @classmethod
    def invalid_name(cls, name: str) -> "InvalidUserNameException":
        return cls(f"El nombre de usuario '{name}' es inválido")
    

class InvalidUserEmailException(UserException):
    @classmethod
    def invalid_user_email(cls, email: str) -> "InvalidUserEmailException":
        return cls(f"El email '{email}' es inválido")


class InvalidRoleException(UserException):
    @classmethod
    def invalid_role(cls, role: str) -> "InvalidRoleException":
        return cls(f"El rol '{role}' es inválido")


class InvalidPhoneNumberException(UserException):
    @classmethod
    def invalid_phone_number(cls, phone_number: str) -> "InvalidPhoneNumberException":
        return cls(f"El número de celular '{phone_number}' es inválido")


class InvalidUserBirthdateException(UserException):
    @classmethod
    def invalid_birthdate(cls, birthdate: date) -> "InvalidUserBirthdateException":
        return cls(f"La fecha de nacimiento {birthdate} es inválida")


class InvalidDniException(UserException):
    @classmethod
    def invalid_dni(cls, dni: str) -> "InvalidDniException":
        return cls(f"El dni '{dni}' es inválido.")