from core.user import UserAccount, Role, UserAccountFactory, RoleFactory, EmployeeAccount
from .dto import SignUpDto, UserDto, RoleDto, CreateEmployeeDto
from core.user.domain.values import RoleAccess
from typing import Set

class UserMapper:
    '''Mapeador entre usuarios y dtos'''
    @classmethod
    def to_user(cls, dto: SignUpDto) -> UserAccount:
        if isinstance(dto, CreateEmployeeDto):
            return cls._to_employee_user(dto)
        return cls._to_client_user(dto)

    @classmethod
    def to_dto(cls, user: UserAccount) -> UserDto:
        if isinstance(user, EmployeeAccount):
            return cls._from_employee_user(user)
        return cls._from_client_user(user)
    
    @classmethod
    def _to_client_user(cls, dto: SignUpDto) -> UserAccount:
        return UserAccountFactory.create_user(
            phone_number=dto.phone_number,
            email=dto.email,
            password=dto.password,
            name=dto.name,
            birthdate=dto.birthdate,
            gender=dto.gender
        )
    
    @classmethod
    def _to_employee_user(cls, dto: CreateEmployeeDto) -> EmployeeAccount:
        employee = UserAccountFactory.create_employee(
            phone_number=dto.phone_number,
            email=dto.email,
            password=dto.password,
            name=dto.name,
            birthdate=dto.birthdate,
            gender=dto.gender,
            dni=dto.dni,
            address=dto.address,
            photo=dto.photo,
            roles=dto.roles,
            categories=dto.categories
        )
        return employee
    
    @classmethod
    def _from_client_user(cls, user: UserAccount) -> UserDto:
        return UserDto(
            id=user.id,
            phone_number=user.phone_number,
            email=user.email,
            name=user.name,
            birthdate=user.birthdate,
            status=user.status,
            gender=user.gender,
            created_date=user.created_date
        )
    
    @classmethod
    def _from_employee_user(cls, employee: EmployeeAccount) -> UserDto:
        return UserDto(
            id=employee.id,
            dni=employee.dni,
            address=employee.address,
            photo=employee.photo,
            phone_number=employee.phone_number,
            email=employee.email,
            name=employee.name,
            birthdate=employee.birthdate,
            status=employee.status,
            gender=employee.gender,
            created_date=employee.created_date,
            roles=[role for role in employee.roles],
            categories=[category for category in employee.categories]
        )


class RoleMapper:
    '''Mapeador entre roles y dtos'''
    @classmethod
    def to_role(cls, rolename: str, accesses: Set[RoleAccess]) -> Role:
        return RoleFactory.create(name=rolename, accesses=accesses)
    
    @classmethod
    def to_dto(cls, role: Role) -> RoleDto:
        return RoleDto(
            id=role.id,
            name=role.name,
            accesses=list(role.accesses),
            created_date=role.created_date
        )