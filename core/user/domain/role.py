from pydantic import BaseModel, model_validator
from datetime import date
from typing import ClassVar
from core.common import PatternMatcher, ID
from core.common.exceptions import InvalidIdException
from core.user.domain.exceptions import InvalidUserNameException
from core.user.domain.events import RoleUpdated, RoleCreated

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
        if not ID.validate(id):
            raise InvalidIdException.invalid_id(id)
        
        if not PatternMatcher.match(self.name):
            raise InvalidUserNameException.invalid_name(self.name)
        
        return self
    
    def rename(self, name: str) -> None:
        '''Renombra el rol'''

        if not PatternMatcher.match(self.name):
            raise InvalidUserNameException.invalid_name(self.name)

        self.name = name
        self.validate_data()
        RoleUpdated(role = self)
        pass
    

class RoleFactory:
    @staticmethod
    def create(name: str) -> Role:
        '''Crea un nuevo rol'''

        role_id = ID.generate()
        created_date = date.today()
        role: Role(id = role_id, name = name, created_date = created_date)
        RoleCreated(role = role)
        return role
    
    @staticmethod
    def load(id: str, name: str, created_date: date) -> Role:
        '''Carga un rol existente'''
        
        role: Role(id = id, name = name, created_date = created_date)
        return role