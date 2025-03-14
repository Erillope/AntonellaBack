from core.common.abstract_repository import GetModel, SaveModel, DeleteModel
from typing import List, Optional, Tuple, TypeVar, Type, Any
from core.common import OrdenDirection, EventSubscriber, Event

Model = TypeVar('Model')

class GetMock(GetModel[Model]):
    def __init__(self) -> None:
        self.exists_input_return_values: List[Tuple[str, bool]]= []
        self.get_input_return_values : List[Tuple[str, Model]] = []
        self.filter_input_return_values : List[Tuple[List[Any], List[Model]]] = []
        self.get_all_return_value : List[Model] = []
    
    def exists(self, id: str) -> bool:
        for _id, return_value in self.exists_input_return_values:
            if _id == id:
                return return_value
        return False
    
    def get(self, id: str) -> Model:
        for _id, model in self.get_input_return_values:
            if _id == id:
                return model
        return
    
    def get_all(self) -> List[Model]:
        return self.get_all_return_value
    
    def filter(self, expresion: Optional[str], order_by: str, direction: OrdenDirection,
               limit: Optional[int]=None, offset: Optional[int]=None) -> List[Model]:
        for input_values, return_values in self.filter_input_return_values:
            if [expresion, order_by, direction, limit, offset] == input_values:
                return return_values
        return []