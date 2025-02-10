from pydantic import BaseModel, model_validator
from datetime import date
from core.common import ID, EventPublisher, Event
from .values import ServiceStatus, ServiceType
from typing import Optional

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
        #TODO
        pass
    
    def change_data(self, name: Optional[str]=None, description: Optional[str]=None,
                    status: Optional[ServiceStatus]=None, type: Optional[ServiceType]=None) -> None:
        '''Cambia los datos del servicio de tienda'''
        #TODO
        pass
    
    def save(self) -> None:
        pass
    
    def delete(self) -> None:
        pass


class StoreServiceFactory:
    @staticmethod
    def create(name: str, description: str, type: ServiceType) -> StoreService:
        #TODO
        store_service: StoreService
        return store_service
    
    @staticmethod
    def load(id: str, name: str, description: str, status: ServiceStatus, type: ServiceType, created_date: date) -> StoreService:
        #TODO
        store_service: StoreService
        return store_service