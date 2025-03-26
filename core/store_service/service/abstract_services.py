from abc import ABC, abstractmethod
from .dto import (StoreServiceDto, CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto,
                  CreateQuestionDto, QuestionDto, UpdateQuestionDto)
from typing import List, Optional

class AbstractStoreServices(ABC):
    @abstractmethod
    def create(self, dto: CreateStoreServiceDto) -> StoreServiceDto: ...
    
    @abstractmethod
    def update(self, dto: UpdateStoreServiceDto) -> StoreServiceDto: ...
    
    @abstractmethod
    def delete(self, id: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def find(self, id: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def filter(self, dto: FilterStoreServiceDto) -> List[StoreServiceDto]: ...


class AbstractQuestionService(ABC):
    @abstractmethod
    def create(self, service_id: str, dto: CreateQuestionDto) -> QuestionDto: ...
    
    @abstractmethod
    def update(self, dto: UpdateQuestionDto) -> QuestionDto: ...
    
    @abstractmethod
    def delete(self, id: str) -> QuestionDto: ...
    
    @abstractmethod
    def find(self, id: str) -> QuestionDto: ...
    
    @abstractmethod
    def service_questions(self, service_id: str) -> List[QuestionDto]: ...