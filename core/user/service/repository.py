from core.common.abstract_repository import GetModel
from core.user import UserAccount
from abc import ABC, abstractmethod
from typing import List

class GetUser(GetModel[UserAccount], ABC):
    @abstractmethod
    def exists_super_admin(self) -> bool: ...
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[UserAccount]: ...