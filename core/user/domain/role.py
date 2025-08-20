from pydantic import BaseModel, model_validator
from datetime import date
from typing import ClassVar
from core.common import PatternMatcher, ID
from core.user.domain.exceptions import InvalidRoleException
from core.user.domain.events import RoleSaved, RoleDeleted
from core.common.events import EventPublisher
from .values import RoleAccess, AccessType, PermissionType
from typing import Set

class Role(BaseModel):
    '''Roles que serán asignados a los usuarios'''
    id: str
    name: str
    accesses: Set[RoleAccess]
    created_date: date
    REGREX: ClassVar[str] = r"^[a-zA-Z0-9_]{3,20}$"
    MATCHER: ClassVar[PatternMatcher] = PatternMatcher(pattern=REGREX)
    SUPER_ADMIN: ClassVar[str] = "super_admin"
    
    @model_validator(mode='after')
    def constructor(self) -> 'Role':
        '''Valida los datos del rol'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        if not self.MATCHER.match(self.name):
            raise InvalidRoleException.invalid_role(self.name)
        
    def rename(self, name: str) -> None:
        '''Renombra el rol'''
        self.name = name
        self._validate_data()
    
    def add_access(self, access_type: AccessType, permission: PermissionType) -> None:
        for access in self.accesses:
            if access.access_type == access_type:
                access.permissions.add(permission)
                return
        self.accesses.add(RoleAccess(access_type=access_type, permissions={permission}))
    
    def set_accesses(self, accesses: Set[RoleAccess]) -> None:
        self.accesses = accesses
        
    def save(self, update: bool=False) -> None:
        EventPublisher.publish(RoleSaved(role=self, update=update))
    
    def delete(self) -> None:
        EventPublisher.publish(RoleDeleted(rolename=self.name))

class RoleFactory:
    @staticmethod
    def create(name: str, accesses: Set[RoleAccess]) -> Role:
        '''Crea un nuevo rol'''
        return Role(id = ID.generate(), name = name, created_date = date.today(), accesses=accesses)
    
    @staticmethod
    def load(id: str, name: str, created_date: date, accesses: Set[RoleAccess]) -> Role:
        '''Carga un rol existente'''
        return Role(id = id, name = name, created_date = created_date, accesses=accesses)