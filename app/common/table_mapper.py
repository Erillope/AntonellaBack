from abc import ABC, abstractmethod
from django.db import models #type: ignore
from typing import Generic, TypeVar

Table = TypeVar('Table', bound=models.Model)
Model = TypeVar('Model')

class TableMapper(Generic[Table, Model], ABC):
    @abstractmethod
    def to_model(self, table: Table) -> Model: ...

    @abstractmethod
    def to_table(self, model: Model) -> Table: ...