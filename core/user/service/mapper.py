from core.user import UserAccount, Role
from .dto import SignUpDto, UserDto, RoleDto

class UserMapper:
    '''Mapeador entre usuarios y dtos'''
    def to_user(self, dto: SignUpDto) -> UserAccount:
        #TODO
        user: UserAccount
        return user

    def to_dto(self, user: UserAccount) -> UserDto:
        #TODO
        dto: UserDto
        return dto


class RoleMapper:
    '''Mapeador entre roles y dtos'''
    def to_role(self, rolename: str) -> Role:
        #TODO
        role: Role
        return role
    
    def to_dto(self, role: Role) -> RoleDto:
        #TODO
        dto: RoleDto
        return dto