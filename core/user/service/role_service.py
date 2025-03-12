from .abstract_services import AbstractRoleService
from .dto import RoleDto
from typing import List, Optional
from core.user import Role
from core.user.domain.values import RoleAccess
from core.common.abstract_repository import GetModel
from .mapper import RoleMapper

class RoleService(AbstractRoleService):
    def __init__(self, get_role: GetModel[Role]):
        self.get_role = get_role
    
    def init(self) -> None:
        if not self.get_role.exists(Role.SUPER_ADMIN):
            self.create(Role.SUPER_ADMIN, RoleAccess.all())
    
    def get(self, role: str) -> RoleDto:
        return RoleMapper.to_dto(self.get_role.get(role))
    
    def create(self, name: str, accesses: List[RoleAccess]) -> RoleDto:
        role = RoleMapper.to_role(name, set(accesses))
        role.save()
        return RoleMapper.to_dto(role)

    def update(self, role: str, new_name: Optional[str]=None, accesses: Optional[List[RoleAccess]]=None) -> RoleDto:
        role_model = self.get_role.get(role)
        if new_name:
            role_model.rename(new_name)
        if accesses:
            role_model.set_accesses(set(accesses))
        role_model.save(update=True)
        return RoleMapper.to_dto(role_model)

    def get_all(self) -> List[RoleDto]:
        roles = self.get_role.get_all()
        return [RoleMapper.to_dto(role) for role in roles]

    def delete(self, role: str) -> RoleDto:
        role_model = self.get_role.get(role)
        role_model.delete()
        return RoleMapper.to_dto(role_model)