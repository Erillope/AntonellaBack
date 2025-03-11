from core.common.abstract_repository import GetModel
from core.user import UserAccount
from abc import ABC, abstractmethod

class GetUser(GetModel[UserAccount], ABC):
    @abstractmethod
    def exists_super_admin(self) -> bool: ...