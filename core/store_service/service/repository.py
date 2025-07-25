from core.common.abstract_repository import GetModel
from core.store_service import Question, StoreService
from abc import ABC, abstractmethod
from typing import List, Optional

class GetQuestion(GetModel[Question], ABC):
    @abstractmethod
    def get_service_questions(self, service_id: str) -> List[Question]: ...


class GetService(GetModel[StoreService], ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> List[StoreService]: ...
    
    @abstractmethod
    def find_by_type(self, type: str) -> List[StoreService]: ...
    
    @abstractmethod
    def prepare_service_type_filter(self, type: str) -> None: ...
    
    @abstractmethod
    def prepare_service_name_filter(self, name: str) -> None: ...
    
    @abstractmethod
    def get_filtered_services(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[StoreService]: ...

    @abstractmethod
    def get_stars(self, service_id: str) -> float: ...