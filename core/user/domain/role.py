from pydantic import BaseModel, model_validator
from datetime import date
from typing import ClassVar
from core.common import PatternMatcher, ID
from core.user.domain.exceptions import InvalidRoleException
from core.user.domain.events import RoleSaved
from core.common.events import EventPublisher

class Role(BaseModel):
    '''Roles que serán asignados a los usuarios'''
    id: str
    name: str
    created_date: date
    REGREX: ClassVar[str] = r"^[a-zA-Z0-9_]{3,20}$"
    MATCHER: ClassVar[PatternMatcher] = PatternMatcher(pattern=REGREX)
    
    @model_validator(mode='after')
    def constructor(self) -> 'Role':
        '''Valida los datos del rol'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.name = self.name.lower()
        ID.validate(self.id)
        if not self.MATCHER.match(self.name):
            raise InvalidRoleException.invalid_role(self.name)
        
    def rename(self, name: str) -> None:
        '''Renombra el rol'''
        self.name = name
        self._validate_data()
    
    def save(self) -> None:
        EventPublisher.publish(RoleSaved(role=self))

class RoleFactory:
    @staticmethod
    def create(name: str) -> Role:
        '''Crea un nuevo rol'''
        return Role(id = ID.generate(), name = name, created_date = date.today())
    
    @staticmethod
    def load(id: str, name: str, created_date: date) -> Role:
        '''Carga un rol existente'''
        return Role(id = id, name = name, created_date = created_date)