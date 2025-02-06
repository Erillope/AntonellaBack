from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional, List
from core.common import ID
from .values import AccountStatus, Gender
from .role import Role

class UserAccount(BaseModel):
    '''Cuenta de usuario'''
    id: str
    phone_number: str
    email: str
    name: str
    password: str
    status: AccountStatus
    gender: Gender
    birthdate: date
    created_date: date
    roles: List[Role]
    
    @model_validator(mode='after')
    def validate_data(self) -> 'UserAccount':
        '''Valida los datos de la cuenta de usuario'''
        #---Usa las clases ID del modulo common, tambien usa las clases en el archivo values para validar el 
        # email, password, etc. No olvides encriptar la contraseña (Borrar este comentario luego de implementar)
        #TODO
        return self
    
    def change_data(self, phone_number: Optional[str]=None, email: Optional[str]=None,
                    name: Optional[str]=None, password: Optional[str]=None,
                    status: Optional[AccountStatus]=None) -> None:
        '''Cambia los datos de la cuenta de usuario'''
        #---No olvides validar los datos, puedes reutilizar el método validate_data, tampoco olvides validar 
        # los datos nulos y lanzar los eventos correspondientes (Borrar este comentario luego de implementar)
        #TODO
        pass
    
    def add_role(self, role: Role) -> None:
        '''Añade un rol a la cuenta de usuario'''
        #TODO
        pass
    
    def remove_role(self, role: Role) -> None:
        '''Remueve un rol de la cuenta de usuario'''
        #TODO
        pass
    
    def verify_password(self, password: str) -> bool:
        '''Verifica la contraseña de la cuenta de usuario'''
        #Recuerda la contraseña del usuario está encriptada, por lo que debes usar el método de verificacion 
        # de UserPassword para compararla
        #TODO
        return False
    
    def verify_account(self, phone_number: str, password: str) -> bool:
        '''Verifica la cuenta de usuario'''
        #TODO
        return False
    
    
class UserAccountBuilder(BaseModel):
    '''Constructor de cuentas de usuario'''
    id: str = ID.generate()
    phone_number: str
    email: str
    name: str
    password: str
    status: AccountStatus = AccountStatus.ENABLE
    birthdate: date
    created_date: date = date.today()
    roles: List[Role]
    
    def set_id(self, id: str) -> 'UserAccountBuilder':
        self.id = id
        return self

    def set_status(self, status: AccountStatus) -> 'UserAccountBuilder':
        self.status = status
        return self
    
    def set_created_date(self, created_date: date) -> 'UserAccountBuilder':
        self.created_date = created_date
        return self
    
    def build(self) -> UserAccount:
        return UserAccount(**self.model_dump())


class UserAccountFactory:
    @staticmethod
    def create(phone_number: str, email: str, name: str, password: str, birthdate: date, gender: Gender,
               roles: Optional[List[Role]] = None) -> UserAccount:
        #Crearás una nueva cuenta de usuario, entonces solo necesitas los datos que te pasan, el resto de
        # parámetros como el id y la fecha las tienes que generar automaticamente, la fecha de creación debe
        # ser la de hoy. Al ser una nueva cuenta, debes lanzar el evento correspondiente, usa la clase constructora
        user : UserAccount
        return user
    
    @staticmethod
    def load(id: str, phone_number: str, email: str, name: str, password: str, status: AccountStatus, 
             birthdate: date, created_date: date, gender: Gender, roles: List[Role]) -> UserAccount:
        '''Carga una cuenta de usuario existente'''
        #Cargarás una cuenta de usuario existente, entonces usa los parámetros que te pasan para crear la #cuenta, no necesitas lanzar un evento porque no estás creando una nueva cuenta. Usa la clase constructora
        #TODO
        user : UserAccount
        return user