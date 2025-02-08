from core.user import UserAccount, Role, UserAccountFactory, RoleFactory
from .dto import SignUpDto, UserDto, RoleDto
from typing import List

class UserMapper:
    '''Mapeador entre usuarios y dtos'''
    @classmethod
    def to_user(cls, dto: SignUpDto) -> UserAccount:
        return UserAccountFactory.create(
            phone_number=dto.phone_number,
            email=dto.email,
            password=dto.password,
            name=dto.name,
            birthdate=dto.birthdate,
            gender=dto.gender
        )

    @classmethod
    def to_dto(cls, user: UserAccount) -> UserDto:
        return UserDto(
            id=user.id,
            phone_number=user.phone_number,
            email=user.email,
            name=user.name,
            birthdate=user.birthdate,
            status=user.status,
            gender=user.gender,
            roles=[RoleMapper.to_dto(role) for role in user.roles],
            created_date=user.created_date,
        )


class RoleMapper:
    '''Mapeador entre roles y dtos'''
    @classmethod
    def to_role(cls, rolename: str) -> Role:
        return RoleFactory.create(name=rolename)
    
    @classmethod
    def to_dto(cls, role: Role) -> RoleDto:
        return RoleDto(
            id=role.id,
            name=role.name,
            created_date=role.created_date
        )