from abc import ABC, abstractmethod
from .dto import UserDto, SignUpDto, UpdateUserDto, FilterUserDto, RoleDto
from typing import List

class AbstractAuthService(ABC):
    @abstractmethod
    def sign_up(self, dto: SignUpDto) -> UserDto: ...
    
    @abstractmethod
    def sign_in(self, phone_number: str, password: str) -> UserDto: ...


class AbstractUpdateUserService(ABC):
    @abstractmethod
    def update_user(self, dto: UpdateUserDto) -> UserDto: ...
    
    @abstractmethod
    def add_role(self, user_id: str, role: str) -> UserDto: ...
    
    @abstractmethod
    def remove_role(self, user_id: str, role: str) -> UserDto: ...


class AbstractFilterUserService(ABC):
    @abstractmethod
    def filter_user(self, dto: FilterUserDto) -> List[UserDto]: ...


class AbstractRoleService(ABC):
    @abstractmethod
    def create(self, name: str) -> RoleDto: ...
    
    @abstractmethod
    def rename(self, role: str, name: str) -> RoleDto: ...
    
    @abstractmethod
    def get_all(self) -> List[RoleDto]: ...
    
    @abstractmethod 
    def delete(self, role: str) -> RoleDto: ...