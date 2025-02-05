from core.user import UserAccount, Role
from .dto import SignUpDto, UserDto, RoleDto

class UserMapper:
    '''Mapeador entre usuarios y dtos'''
    @staticmethod
    def to_user(dto: SignUpDto) -> UserAccount:
        #TODO
        user: UserAccount
        return user

    @staticmethod
    def to_dto(user: UserAccount) -> UserDto:
        #TODO
        dto: UserDto
        return dto


class RoleMapper:
    '''Mapeador entre roles y dtos'''
    @staticmethod
    def to_role(rolename: str) -> Role:
        #TODO
        role: Role
        return role
    
    @staticmethod
    def to_dto(role: Role) -> RoleDto:
        #TODO
        dto: RoleDto
        return dto