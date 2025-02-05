from .abstract_services import AbstractRoleService
from .dto import RoleDto
from typing import List
from core.user import Role
from core.common.abstract_repository import GetModel, DeleteModel

class RoleService(AbstractRoleService):
    def __init__(self, get_role: GetModel[Role], delete_role: DeleteModel[Role]):
        self.get_role = get_role
        self.delete_role = delete_role
    
    def create(self, name: str) -> RoleDto:
        #TODO
        role_dto: RoleDto
        return role_dto

    def rename(self, role: str, name: str) -> RoleDto:
        #TODO
        role_dto: RoleDto
        return role_dto

    def get_all(self) -> List[RoleDto]:
        #TODO
        role_dto: List[RoleDto]
        return role_dto

    def delete(self, role: str) -> RoleDto:
        #TODO
        role_dto: RoleDto
        return role_dto