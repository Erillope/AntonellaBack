from .abstract_services import (AbstractAuthService, AbstractUpdateUserService,
                                AbstractFilterUserService)
from .dto import SignUpDto, UserDto, UpdateUserDto, FilterUserDto
from core.common.abstract_repository import GetModel
from core.user import UserAccount
from typing import List
from pydantic import BaseModel

class AuthService(BaseModel, AbstractAuthService):
    get_user: GetModel[UserAccount]
    
    def sign_up(self, dto: SignUpDto) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto

    def sign_in(self, phone_number: str, password: str) -> UserDto:
        #TODO
        user_dto: UserDto
        return user_dto


class UpdateUserService(BaseModel, AbstractUpdateUserService):
    get_user: GetModel[UserAccount]
    
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


class FilterUserService(BaseModel, AbstractFilterUserService):
    get_user: GetModel[UserAccount]
    
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]:
        #TODO
        user_dto: List[UserDto]
        return user_dto