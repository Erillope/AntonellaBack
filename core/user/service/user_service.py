from .abstract_services import (AbstractAuthService, AbstractUpdateUserService,
                                AbstractFilterUserService)
from .dto import SignUpDto, UserDto, UpdateUserDto, FilterUserDto
from core.common.abstract_repository import GetModel
from core.user import UserAccount
from typing import List
from pydantic import BaseModel

class AuthService(AbstractAuthService):
    def __init__(self, get_user: GetModel[UserAccount]):
        self.get_user = get_user
    
    def sign_up(self, dto: SignUpDto) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto

    def sign_in(self, phone_number: str, password: str) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto


class UpdateUserService(AbstractUpdateUserService):
    def __init__(self, get_user: GetModel[UserAccount]):
        self.get_user = get_user
    
    def update_user(self, dto: UpdateUserDto) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto

    def add_role(self, user_id: str, role: str) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto

    def remove_role(self, user_id: str, role: str) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto


class FilterUserService(AbstractFilterUserService):
    def __init__(self, get_user: GetModel[UserAccount]):
        self.get_user = get_user
    
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]:
        #TODO
        user_dto: List[UserDto]
        return user_dto