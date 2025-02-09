from .abstract_services import (AbstractAuthService, AbstractUpdateUserService,
                                AbstractFilterUserService)
from .dto import SignUpDto, UserDto, UpdateUserDto, FilterUserDto
from .exceptions import AlreadyExistsUserException, IncorrectPasswordException
from .mapper import UserMapper
from core.common.abstract_repository import GetModel
from core.user import UserAccount, Role
from typing import List

class AuthService(AbstractAuthService):
    def __init__(self, get_user: GetModel[UserAccount], get_role: GetModel[Role]):
        self.get_user = get_user
        self.get_role = get_role
    
    def sign_up(self, dto: SignUpDto) -> UserDto:
        if self.get_user.exists(dto.phone_number):
            raise AlreadyExistsUserException.already_exists(dto.phone_number)
        if self.get_user.exists(dto.email):
            raise AlreadyExistsUserException.already_exists(dto.email)
        user = UserMapper.to_user(dto)
        for role in dto.roles:
            role_model = self.get_role.get(role)
            user.add_role(role_model)
        user.save()
        return UserMapper.to_dto(self.get_user.get(user.id))

    def sign_in(self, phone_number: str, password: str) -> UserDto:
        user = self.get_user.get(phone_number)
        if not user.verify_account(phone_number, password):
            raise IncorrectPasswordException.incorrect_password()
        return UserMapper.to_dto(user)


class UpdateUserService(AbstractUpdateUserService):
    def __init__(self, get_user: GetModel[UserAccount], get_role: GetModel[Role]):
        self.get_user = get_user
        self.get_role = get_role
    
    def update_user(self, dto: UpdateUserDto) -> UserDto:
        if dto.phone_number and self.get_user.exists(dto.phone_number):
            raise AlreadyExistsUserException.already_exists(dto.phone_number)
        if dto.email and self.get_user.exists(dto.email):
            raise AlreadyExistsUserException.already_exists(dto.email)
        user = self.get_user.get(dto.id)
        user.change_data(dto.phone_number, dto.email, dto.name, dto.password, dto.status)
        user.save()
        return UserMapper.to_dto(self.get_user.get(user.id))

    def add_role(self, user_id: str, role: str) -> UserDto:
        user = self.get_user.get(user_id)
        role_model = self.get_role.get(role)
        user.add_role(role_model)
        user.save()
        return UserMapper.to_dto(self.get_user.get(user.id))

    def remove_role(self, user_id: str, role: str) -> UserDto:
        user = self.get_user.get(user_id)
        role_model = self.get_role.get(role)
        user.remove_role(role_model)
        user.save()
        return UserMapper.to_dto(self.get_user.get(user.id))


class FilterUserService(AbstractFilterUserService):
    def __init__(self, get_user: GetModel[UserAccount]):
        self.get_user = get_user
    
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]:
        users = self.get_user.filter(dto.expresion, dto.order_by, dto.order_direction, dto.limit, dto.offset)
        return [UserMapper.to_dto(user) for user in users]