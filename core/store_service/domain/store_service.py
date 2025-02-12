from pydantic import BaseModel, model_validator
from datetime import date
from core.common import ID, EventPublisher, Event
from .values import ServiceStatus, ServiceType, ServiceName
from typing import Optional
from .events import StoreServiceDeleted, StoreServiceSaved

class StoreService(BaseModel):
    "Servicio de tienda"
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    created_date: date
    
    @model_validator(mode='after')
    def validate_data(self) -> 'StoreService':
        '''Valida los datos del servicio de tienda'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.name = self.name.lower()
        self.description = self.description.lower()
        ID.validate(self.id)
        ServiceName.MATCHER.validate(self.name)
        pass
    
    def change_data(self, name: Optional[str]=None, description: Optional[str]=None,
                    status: Optional[ServiceStatus]=None, type: Optional[ServiceType]=None) -> None:
        '''Cambia los datos del servicio de tienda'''
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if status is not None:
            self.status = status

        if type is not None:
            self.type = type
        
        pass
    
    def save(self) -> None:
        EventPublisher.publish(StoreServiceSaved(service = self))
        for event in self._events:
            EventPublisher.publish(event)
        self._events.clear()
        pass
    
    def delete(self) -> None:
        EventPublisher.publish(StoreServiceDeleted(service = self))
        pass


class StoreServiceFactory:
    @staticmethod
    def create(name: str, description: str, type: ServiceType) -> StoreService:
        #TODO
        return StoreService(
            id = ID.generate(),
            name = name,
            description = description,
            status = ServiceStatus.ENABLE,
            type = type,
            created_date = date.today()
        )
    
    @staticmethod
    def load(id: str, name: str, description: str, status: ServiceStatus, type: ServiceType, created_date: date) -> StoreService:
        #TODO
        return StoreService(
            id = id,
            name = name,
            description = description,
            status = status,
            type = type,
            created_date = created_date
        )