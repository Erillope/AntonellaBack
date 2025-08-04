from core.common.abstract_repository import GetModel
from core.store_service import Question, StoreService
from abc import ABC, abstractmethod
from .dto import FilterStoreServiceDto
from typing import List, Optional, Tuple

class GetQuestion(GetModel[Question], ABC):
    @abstractmethod
    def get_service_questions(self, service_id: str) -> List[Question]: ...


class GetService(GetModel[StoreService], ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> List[StoreService]: ...
    
    @abstractmethod
    def find_by_type(self, type: str) -> List[StoreService]: ...

    @abstractmethod
    def filter_services(self, filter_dto: FilterStoreServiceDto) -> Tuple[List[StoreService], int]: ...

    @abstractmethod
    def get_stars(self, service_id: str) -> float: ...