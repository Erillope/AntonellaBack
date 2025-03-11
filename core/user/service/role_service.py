from .abstract_services import AbstractRoleService
from .dto import RoleDto
from typing import List
from core.user import Role
from core.common.abstract_repository import GetModel
from .mapper import RoleMapper
from .exceptions import AlreadyExistsRoleException

class RoleService(AbstractRoleService):
    def __init__(self, get_role: GetModel[Role]):
        self.get_role = get_role
    
    def init(self) -> None:
        if not self.get_role.exists(Role.SUPER_ADMIN):
            self.create(Role.SUPER_ADMIN)
        
    def create(self, name: str) -> RoleDto:
        if self.get_role.exists(name):
            raise AlreadyExistsRoleException.already_exists(name)
        role = RoleMapper.to_role(name)
        role.save()
        return RoleMapper.to_dto(role)

    def rename(self, role: str, name: str) -> RoleDto:
        if self.get_role.exists(name):
            raise AlreadyExistsRoleException.already_exists(name)
        role_model = self.get_role.get(role)
        role_model.rename(name)
        role_model.save()
        return RoleMapper.to_dto(role_model)

    def get_all(self) -> List[RoleDto]:
        roles = self.get_role.get_all()
        return [RoleMapper.to_dto(role) for role in roles]

    def delete(self, role: str) -> RoleDto:
        role_model = self.get_role.get(role)
        role_model.delete()
        return RoleMapper.to_dto(role_model)