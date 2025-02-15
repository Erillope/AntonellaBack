from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date
from .values import ServiceStatus, ServiceType, ServiceName
from .events import StoreServiceDeleted, StoreServiceSaved, StoreServiceImageAdded, StoreServiceImageDeleted
from core.common import ID, EventPublisher, Event
from typing import Optional, List
from core.common.image_storage import Base64ImageStorage

class StoreService(BaseModel):
    "Servicio de tienda"
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    images: List[str] = []
    created_date: date
    _events: List[Event] = PrivateAttr(default=[])
    
    @model_validator(mode='after')
    def validate_data(self) -> 'StoreService':
        '''Valida los datos del servicio de tienda'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.name = self.name.lower().strip()
        self.description = self.description.lower()
        ID.validate(self.id)
        ServiceName.validate(self.name)
    
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
        
        self._validate_data()
    
    def add_image(self, image: Base64ImageStorage) -> None:
        '''Agrega una imagen al servicio de tienda'''
        self.images.append(image.get_url())
        self._events.append(StoreServiceImageAdded(store_service_id=self.id, image=image))

    def delete_image(self, image_url: str) -> None:
        '''Elimina una imagen del servicio de tienda'''
        self.images.remove(image_url)
        self._events.append(StoreServiceImageDeleted(store_service_id=self.id, image_url=image_url))
    
    def save(self) -> None:
        EventPublisher.publish(StoreServiceSaved(store_service= self))
        for event in self._events:
            EventPublisher.publish(event)
        self._events.clear()
    
    def delete(self) -> None:
        EventPublisher.publish(StoreServiceDeleted(store_service_id = self.id))


class StoreServiceFactory:
    @staticmethod
    def create(name: str, description: str, type: ServiceType) -> StoreService:
        return StoreService(
            id = ID.generate(),
            name = name,
            description = description,
            status = ServiceStatus.ENABLE,
            type = type,
            created_date = date.today(),
        )
    
    @staticmethod
    def load(id: str, name: str, description: str, status: ServiceStatus, type: ServiceType, created_date: date, images: List[str]) -> StoreService:
        return StoreService(
            id = id,
            name = name,
            description = description,
            status = status,
            type = type,
            images = images,
            created_date = created_date,
        )