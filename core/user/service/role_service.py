from .abstract_services import AbstractRoleService
from .dto import RoleDto
from typing import List
from core.user import Role
from core.common.abstract_repository import GetModel, DeleteModel
from pydantic import BaseModel

class RoleService(BaseModel, AbstractRoleService):
    get_role: GetModel[Role]
    delete_role: DeleteModel[Role]
    
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

    def delete(self, role: str) -> None:
        #TODO
        pass