from .abstract_services import (AbstractAuthService, AbstractUpdateUserService,
                                AbstractFilterUserService)
from .dto import SignUpDto, UserDto, UpdateUserDto, FilterUserDto, CreateEmployeeDto
from .exceptions import IncorrectPasswordException, AlreadyExistsSuperAdminException
from .mapper import UserMapper
from core.common.abstract_repository import GetModel
from .repository import GetUser
from core.user import UserAccount, Role
from typing import List
from core.common.config import AppConfig
from core.common.email import EmailHost, EmailMessage
from core.token import AbstractTokenService
from core.token import Token
from datetime import timedelta

class AuthService(AbstractAuthService):    
    def __init__(self, get_user: GetUser, get_role: GetModel[Role], email_host: EmailHost,
                 token_service: AbstractTokenService):
        self.get_user = get_user
        self.get_role = get_role
        self.email_host = email_host
        self.token_service = token_service
    
    def init(self) -> None:
        if not self.get_user.exists_super_admin():
            super_admin_data = CreateEmployeeDto(**AppConfig.default_super_admin())
            self.sign_up(super_admin_data)
            
    def sign_up(self, dto: SignUpDto) -> UserDto:
        self._validate_unique_super_admin(dto)
        user = UserMapper.to_user(dto)
        user.save()
        return UserMapper.to_dto(user)

    def sign_in(self, phone_number: str, password: str) -> UserDto:
        user = self.get_user.get(phone_number)
        if not user.verify_account(phone_number, password):
            raise IncorrectPasswordException.incorrect_password()
        return UserMapper.to_dto(user)
    
    def create_change_password_token(self, email: str) -> Token:
        user = self.get_user.get(email)
        token = self.token_service.create(timedelta(minutes=30), user.id)
        message = EmailMessage(
            to=user.email,
            subject='Cambio de contraseña',
            body=AppConfig.reset_password_message(user.name, token.id) 
        )
        self.email_host.send_email(message)
        return token

    def _validate_unique_super_admin(self, dto: SignUpDto) -> None:
        if not isinstance(dto, CreateEmployeeDto): return
        if not Role.SUPER_ADMIN in dto.roles: return
        if not self.get_user.exists_super_admin(): return
        raise AlreadyExistsSuperAdminException.already_exists()


class UpdateUserService(AbstractUpdateUserService):
    def __init__(self, get_user: GetModel[UserAccount], get_role: GetModel[Role],
                 token_service: AbstractTokenService):
        self.token_service = token_service
        self.get_user = get_user
        self.get_role = get_role
    
    def update_user(self, dto: UpdateUserDto) -> UserDto:
        user = self.get_user.get(dto.id)
        user.change_data(dto.phone_number, dto.email, dto.name, dto.password, dto.status)
        user.save(update=True)
        return UserMapper.to_dto(self.get_user.get(user.id))

    def change_password_with_token(self, token_id: str, password: str) -> UserDto:
        token = self.token_service.get(token_id)
        user = self.get_user.get(token.user_id)
        user.change_data(password=password)
        user.save(update=True)
        token.delete()
        return UserMapper.to_dto(user)
        
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
    def __init__(self, get_user: GetUser):
        self._get_user = get_user
    
    def get_user(self, user_id: str) -> UserDto:
        user = self._get_user.get(user_id)
        return UserMapper.to_dto(user)
    
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]:
        users = self._get_user.filter(dto.order_by, dto.order_direction, dto.limit, dto.offset, dto.fields)
        return [UserMapper.to_dto(user) for user in users]
    
    def get_by_role(self, role: str) -> List[UserDto]:
        users = self._get_user.get_by_role(role)
        return [UserMapper.to_dto(user) for user in users]