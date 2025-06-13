from abc import ABC, abstractmethod
from .dto import UserDto, SignUpDto, UpdateUserDto, FilterUserDto, RoleDto
from typing import List, Optional
from core.token.tokens import Token
from core.user.domain.values import RoleAccess

class AbstractAuthService(ABC):
    @abstractmethod
    def sign_up(self, dto: SignUpDto) -> UserDto: ...
    
    @abstractmethod
    def sign_in(self, phone_number: str, password: str) -> UserDto: ...
    
    @abstractmethod
    def create_change_password_token(self, email: str) -> Token: ...


class AbstractUpdateUserService(ABC):
    @abstractmethod
    def update_user(self, dto: UpdateUserDto) -> UserDto: ...
    
    @abstractmethod
    def change_password_with_token(self, token_id: str, password: str) -> UserDto: ...


class AbstractFilterUserService(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> UserDto: ...
    
    @abstractmethod
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]: ...
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[UserDto]: ...
    
    @abstractmethod
    def get_all(self) -> List[UserDto]: ...


class AbstractRoleService(ABC):
    @abstractmethod
    def get(self, role: str) -> RoleDto: ...
    
    @abstractmethod
    def create(self, name: str, accesses: List[RoleAccess]) -> RoleDto: ...
    
    @abstractmethod
    def update(self, role: str, new_name: Optional[str]=None, accesses: Optional[List[RoleAccess]]=None) -> RoleDto: ...
    
    @abstractmethod
    def get_all(self) -> List[RoleDto]: ...
    
    @abstractmethod 
    def delete(self, role: str) -> RoleDto: ...