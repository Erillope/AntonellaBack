from enum import Enum
from core.common import PatternMatcher
from datetime import date
from .exceptions import *
import bcrypt

class AccountStatus(str, Enum):
    '''Estados de la cuenta de usuario'''
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class Gender(str, Enum):
    '''Géneros de usuario'''
    MALE = "MASCULINO"
    FEMALE = "FEMENINO"
    OTHER = "OTRO"


class UserPhoneNumber:
    '''Validador de números de teléfono'''
    REGREX = r"^(0)?9\d{8}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidPhoneNumberException.invalid_phone_number(value)
        

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
    REGREX = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidUserEmailException.invalid_user_email(value)


class UserBirthdate:
    '''Validador de fechas de nacimiento de usuario'''
    MAX_AGE = 100
    MIN_AGE = 3
    
    @classmethod
    def validate(cls, value: date) -> None:
        #TODO
        edad = date.today().year - value.year
        if edad >= cls.MAX_AGE or edad <= cls.MIN_AGE:
            raise InvalidUserBirthdateException.invalid_birthdate(value)