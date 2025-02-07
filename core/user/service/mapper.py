from core.user import UserAccount, Role
from .dto import SignUpDto, UserDto, RoleDto

class UserMapper:
    '''Mapeador entre usuarios y dtos'''
    @classmethod
    def to_user(cls, dto: SignUpDto) -> UserAccount:
        #TODO
        user: UserAccount
        return user

    @classmethod
    def to_dto(cls, user: UserAccount) -> UserDto:
        #TODO
        dto: UserDto
        return dto


class RoleMapper:
    '''Mapeador entre roles y dtos'''
    @classmethod
    def to_role(cls, rolename: str) -> Role:
        #TODO
        role: Role
        return role
    
    @classmethod
    def to_dto(cls, role: Role) -> RoleDto:
        #TODO
        dto: RoleDto
        return dto