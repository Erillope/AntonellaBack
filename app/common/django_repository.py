from core.common import OrdenDirection
from core.common.abstract_repository import GetModel, SaveModel, DeleteModel
from .table_mapper import TableMapper
from .exceptions import ModelNotFoundException
from django.db import models #type: ignore
from typing import Type, List, Optional, TypeVar, Generic, Dict
from core.common import ID
Table = TypeVar('Table', bound=models.Model)
Model = TypeVar('Model')

class DjangoGetModel(GetModel[Model], Generic[Table, Model]):
    def __init__(self, table: Type[Table], mapper: TableMapper[Table, Model]) -> None:
        self.table = table
        self.mapper = mapper
        self.allowed_fields : List[str] = []
    
    def exists(self, id: str) -> bool:
        if not ID.is_id(id): return False
        return self.table.objects.filter(id=id).exists()
    
    def get_all(self) ->List[Model]:
        tables = self.table.objects.all()
        return [self.mapper.to_model(table) for table in tables]
    
    def get(self, id: str) -> Model:
        if not self.exists(id):
            raise ModelNotFoundException.not_found(id)
        table = self.table.objects.get(id=id)
        return self.mapper.to_model(table)
    
    def filter(self, order_by: str, direction: OrdenDirection,
               limit: Optional[int]=None, offset: Optional[int]=None, fields: Dict[str, str]={}) -> List[Model]:
        tables = []
        start = 0
        end = 0
        if len(fields) == 0:
            tables = self.table.objects.all()
        if offset: start = offset
        if limit: end = start + limit
        else: end = len(tables)
        tables = self.table.objects.order_by(order_by) if direction == OrdenDirection.ASC else self.table.objects.order_by(f'-{order_by}')
        return [self.mapper.to_model(table) for table in tables[start:end]]


class DjangoSaveModel(SaveModel[Model], Generic[Table, Model]):
    def __init__(self, mapper: TableMapper[Table, Model]) -> None:
        self.mapper = mapper
    
    def save(self, model: Model) -> None:
        table = self.mapper.to_table(model)
        table.save()


class DjangoDeleteModel(DeleteModel[Model], Generic[Table, Model]):
    def __init__(self, table: Type[Table], mapper: TableMapper[Table, Model],
                 get_model: GetModel[Model]) -> None:
        self.mapper = mapper
        self.table = table
        self.get_model = get_model
    
    def delete(self, id: str) -> Model:
        model = self.get_model.get(id)
        table = self.mapper.to_table(model)
        table.delete()
        return model