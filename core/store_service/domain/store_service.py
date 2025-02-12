from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date
from .values import ServiceStatus, ServiceType, ServiceName
from .events import StoreServiceDeleted, StoreServiceSaved, StoreServiceImageAdded, StoreServiceImageDeleted
from core.common import ID, EventPublisher, Event, Base64SaveStorageImage, DeleteStorageImage
from typing import Optional, List, ClassVar

class StoreService(BaseModel):
    "Servicio de tienda"
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    images: List[str] = []
    created_date: date
    IMAGES_FOLDER: ClassVar[str] = 'store_service_images'
    IMAGE_CONVERTER: ClassVar[Base64SaveStorageImage] = Base64SaveStorageImage(IMAGES_FOLDER)
    IMAGE_DELETER: ClassVar[DeleteStorageImage] = DeleteStorageImage(IMAGES_FOLDER)
    _events: List[Event] = PrivateAttr(default=[])
    
    @model_validator(mode='after')
    def validate_data(self) -> 'StoreService':
        '''Valida los datos del servicio de tienda'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.name = self.name.lower()
        self.description = self.description.lower()
        ID.validate(self.id)
        ServiceName.validate(self.name)
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
        
        self._validate_data()
        pass
    
    def add_image(self, base64_image: str) -> None:
        '''Agrega una imagen al servicio de tienda'''
        #TODO
        if image not in self.images: return
        self.images.append(base64_image)
        self._events.append(StoreServiceImageAdded(store_service_id=self.id, image=base64_image))
        pass

    def delete_image(self, image: str) -> None:
        '''Elimina una imagen del servicio de tienda'''
        if image not in self.images: return
        self.images.remove(image)
        self._events.append(StoreServiceImageDeleted(store_service_id=self.id, image=image))
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
    def create(name: str, description: str, type: ServiceType, images: List[str]=[]) -> StoreService:
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
    def load(id: str, name: str, description: str, status: ServiceStatus, type: ServiceType, created_date: date, images: List[str]=[]) -> StoreService:
        #TODO
        return StoreService(
            id = id,
            name = name,
            description = description,
            status = status,
            type = type,
            created_date = created_date
        )