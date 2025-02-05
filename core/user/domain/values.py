from enum import Enum
from core.common import PatternMatcher

class AccountStatus(str, Enum):
    '''Estados de la cuenta de usuario'''
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


class UserPhoneNumber:
    '''Validador de números de teléfono'''
    REGREX = r"^(0)?9\\d{8}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        #---Usa el MATCHER para las validaciones y lanzar las excepciones del archivo exceptions en caso de 
        # que los valores no sean validos (Borrar este comentario luego de implementar)
        #TODO
        pass


class UserPassword:
    '''Validador de contraseñas de usuario'''
    REGREX = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        #TODO
        pass

    @classmethod
    def verify(cls, value: str, password: str) -> bool:
        #TODO
        return False
    
    @classmethod
    def encode(cls, value: str) -> str:
        #TODO
        return ""


class UserName:
    '''Validador de nombres de usuario'''
    REGREX = r"^(?=.{4,16}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        #TODO
        pass


class UserEmail:
    '''Validador de correos electrónicos de usuario'''
    REGREX = r"^[a-zA-Z0-9._%+-]+@gmail\\.com$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        #TODO
        pass


class UserBirthdate:
    '''Validador de fechas de nacimiento de usuario'''
    MAX_AGE = 100
    
    @classmethod
    def validate(cls, value: str) -> None:
        #TODO
        pass