from enum import Enum
from core.common import PatternMatcher
from datetime import date
from .exceptions import *
import bcrypt
from pydantic import BaseModel, model_validator
from typing import List, Set

class AccountStatus(str, Enum):
    '''Estados de la cuenta de usuario'''
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class Gender(str, Enum):
    '''Géneros de usuario'''
    MALE = "MASCULINO"
    FEMALE = "FEMENINO"


class AccessType(str, Enum):
    CITAS = "CITAS"
    USUARIOS = "USUARIOS"
    SERVICIOS = "SERVICIOS"
    PRODUCTOS = "PRODUCTOS"
    NOTIFICACIONES = "NOTIFICACIONES"
    ROLES = "ROLES"
    CHATS = "CHATS"
    PAGOS = "PAGOS"
    MOVIL = "MOVIL"

class PermissionType(str, Enum):
    READ = "READ"
    CREATE = "CREATE"
    DELETE = "DELETE"
    EDIT = "EDIT"


class EmployeeCategories(str, Enum):
    CABELLO = "CABELLO"
    UNAS = "UÑAS"
    SPA = "SPA"
    MAQUILLAJE = "MAQUILLAJE"
    
    
class RoleAccess(BaseModel):
    '''Acceso de un rol a un recurso'''
    access_type: AccessType
    permissions: Set[PermissionType]
    
    @model_validator(mode='after')
    def init(self) -> 'RoleAccess':
        if PermissionType.EDIT in self.permissions or PermissionType.DELETE in self.permissions:
            self.permissions.add(PermissionType.READ)
        return self
        
    @classmethod
    def all(cls) -> List['RoleAccess']:
        return [
            RoleAccess(
                access_type=access,
                permissions={PermissionType.READ, PermissionType.CREATE, PermissionType.EDIT, PermissionType.DELETE}
            )
            for access in AccessType
        ]
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, RoleAccess):
            return self.access_type == value.access_type
        return False

    def __hash__(self) -> int:
        return hash((self.access_type))
    
    
class UserPhoneNumber:
    '''Validador de números de teléfono'''
    REGREX = r"^(0)?9\d{8}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.is_phone_number(value):
            raise InvalidPhoneNumberException.invalid_phone_number(value)
    
    @classmethod
    def is_phone_number(cls, value: str) -> bool:
        return cls.MATCHER.match(value)
        

class UserPassword:
    '''Validador de contraseñas de usuario'''
    REGREX = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    BCRYPT_REGREX = r'^\$2[ayb]\$[0-9]{2}\$[./A-Za-z0-9]{53}$'
    MATCHER = PatternMatcher(pattern=REGREX)
    BCRYPT_MATCHER = PatternMatcher(pattern=BCRYPT_REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidUserPasswordException.invalid_password(value)

    @classmethod
    def verify(cls, hashed: str, password: str) -> bool:
        password_bytes = password.encode()
        return bcrypt.checkpw(password_bytes, hashed.encode())
    
    @classmethod
    def encode(cls, password: str) -> str:
        if cls.is_encoded(password):
            return password
        password_bytes = password.encode()
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
        return hashed.decode()
    
    @classmethod
    def is_encoded(cls, password: str) -> bool:
        return cls.BCRYPT_MATCHER.match(password)


class UserName:
    '''Validador de nombres de usuario'''
    REGREX = r"^(?=.{4,16}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidUserNameException.invalid_name(value)


class UserEmail:
    '''Validador de correos electrónicos de usuario'''
    REGREX = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.is_email(value):
            raise InvalidUserEmailException.invalid_user_email(value)
    
    @classmethod
    def is_email(cls, value: str) -> bool:
        return cls.MATCHER.match(value)


class UserBirthdate:
    '''Validador de fechas de nacimiento de usuario'''
    MAX_AGE = 100
    MIN_AGE = 3
    
    @classmethod
    def validate(cls, value: date) -> None:
        edad = date.today().year - value.year
        if edad >= cls.MAX_AGE or edad <= cls.MIN_AGE:
            raise InvalidUserBirthdateException.invalid_birthdate(value)


class DniValue:
    MATCHER = PatternMatcher(pattern=r'^\d{10}$')
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidDniException.invalid_dni(value)