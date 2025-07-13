from core.common.abstract_repository import GetModel
from core.user import UserAccount
from abc import ABC, abstractmethod
from typing import List, Tuple
from .dto import FilterUserDto

class GetUser(GetModel[UserAccount], ABC):
    @abstractmethod
    def exists_super_admin(self) -> bool: ...
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[UserAccount]: ...
    
    @abstractmethod
    def get_filtered_users(self, filter_data: FilterUserDto) -> Tuple[List[UserAccount], int]: ...