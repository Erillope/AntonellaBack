from pydantic import BaseModel, model_validator
from datetime import date
from typing import ClassVar
from core.common import PatternMatcher

class Role(BaseModel):
    '''Roles que serán asignados a los usuarios'''
    id: str
    name: str
    created_date: date
    REGREX: ClassVar[str] = r"^[a-zA-Z0-9_]{3,20}$"
    MATCHER: ClassVar[PatternMatcher] = PatternMatcher(pattern=REGREX)
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Role':
        '''Valida los datos del rol'''
        #---Usa las clases ID y PatternMatcher del modulo common para validar los datos, no olvides lanzar 
        # excepciones para cuando los datos sean inválidos (Borrar este comentario luego de implementar)
        #TODO
        return self
    
    def rename(self, name: str) -> None:
        '''Renombra el rol'''
        #---No olvides validar los datos, puedes reutilizar el método validate_data, tampoco olvides lanzar 
        # los eventos correspondientes (Borrar este comentario luego de implementar)
        #TODO
        pass
    

class RoleFactory:
    @staticmethod
    def create(name: str) -> Role:
        '''Crea un nuevo rol'''
        #Crearás un nuevo rol, entonces solo necesitas el nombre del rol, el resto de parámetros como el id
        # y la fecha las tienes que generar automaticamente, la fecha de creación debe ser la de hoy.
        #Al ser un nuevo rol, debes lanzar el evento correspondiente
        #TODO
        role: Role
        return role
    
    @staticmethod
    def load(id: str, name: str, created_date: date) -> Role:
        '''Carga un rol existente'''
        #Cargarás un rol existente, entonces usa los parámetros que te pasan para crear el rol
        #No necesitas lanzar un evento porque no estás creando un nuevo rol
        #TODO
        role: Role
        return role