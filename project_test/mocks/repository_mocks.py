from core.common.abstract_repository import GetModel, SaveModel, DeleteModel
from typing import List, Optional, Tuple, TypeVar, Type, Any
from core.common import OrdenDirection, EventSubscriber, Event

Model = TypeVar('Model')

class GetMock(GetModel[Model]):
    def __init__(self) -> None:
        self.get_input_value : str = ''
        self.filter_input_value : List[Any] = []
        self.get_return_value : Model
        self.get_all_return_value : List[Model] = []
        self.filter_return_value : List[Model] = []
        
    def get(self, id: str) -> Model:
        if id == self.get_input_value:
            return self.get_return_value
        return 
    
    def get_all(self) -> List[Model]:
        return self.get_all_return_value
    
    def filter(self, expresion: Optional[str], order_by: str, direction: OrdenDirection,
               limit: Optional[int]=None, offset: Optional[int]=None) -> List[Model]:
        if [expresion, order_by, direction, limit, offset] == self.filter_input_value:
            return self.filter_return_value
        return


class SaveMock(SaveModel[Model], EventSubscriber[Event]):
    def __init__(self, supported_events: Tuple[Type[Event], ...]) -> None:
        self.SUPPORTED_EVENTS = supported_events
        self.saved_model: Model
        
    def save(self, model: Model) -> None:
        self.saved_model = model
    
    def handle(self, event: Event) -> None:
        model = list(event.model_dump().values())[0]
        self.save(model)


class DeleteMock(DeleteModel[Model]):
    def __init__(self) -> None:
        self.delete_input_value: str = ''
        self.deleted_model: Model
        
    def delete(self, id: str) -> Model:
        if id == self.delete_input_value:
            return self.deleted_model
        return