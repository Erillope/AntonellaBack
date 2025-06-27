from core.common.abstract_repository import GetModel
from core.user import UserAccount
from abc import ABC, abstractmethod
from typing import List, Optional

class GetUser(GetModel[UserAccount], ABC):
    @abstractmethod
    def exists_super_admin(self) -> bool: ...
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[UserAccount]: ...
    
    @abstractmethod
    def prepare_service_category_filter(self, service_category: str) -> None: ...
    
    @abstractmethod
    def get_filtered_users(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserAccount]: ...