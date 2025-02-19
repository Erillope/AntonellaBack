from abc import ABC, abstractmethod
from .dto import (StoreServiceDto, CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto,
                  CreateQuestionDto, QuestionDto)
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
    
    @abstractmethod
    def add_image(self, service_id: str, image: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def delete_image(self, service_id: str, image: str) -> StoreServiceDto: ...


class AbstractQuestionService(ABC):
    @abstractmethod
    def create(self, service_id: str, dto: CreateQuestionDto) -> QuestionDto: ...
    
    @abstractmethod
    def update(self, id: str, title: Optional[str]=None) -> QuestionDto: ...
    
    @abstractmethod
    def delete(self, id: str) -> QuestionDto: ...
    
    @abstractmethod
    def find(self, id: str) -> QuestionDto: ...
    
    @abstractmethod
    def add_choice(self, question_id: str, option: str, image: Optional[str]=None) -> QuestionDto: ...
    
    @abstractmethod
    def delete_choice(self, question_id: str, option: str) -> QuestionDto: ...
    
    @abstractmethod
    def service_questions(self, service_id: str) -> List[QuestionDto]: ...