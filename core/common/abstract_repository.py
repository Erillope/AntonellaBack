from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, Dict
from .values import OrdenDirection

Model = TypeVar('Model')

class GetModel(ABC, Generic[Model]):
    @abstractmethod
    def exists(self, id: str) -> bool: ...
    
    @abstractmethod
    def get_all(self) -> List[Model]: ...
    
    @abstractmethod
    def get(self, id: str) -> Model: ...
    
    @abstractmethod
    def total_count(self) -> int: ...


class SaveModel(ABC, Generic[Model]):
    @abstractmethod
    def save(self, model: Model) -> None: ...


class DeleteModel(ABC, Generic[Model]):
    @abstractmethod
    def delete(self, id: str) -> Model: ...