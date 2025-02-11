from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date
from core.common import ID, EventPublisher, Event, Base64SaveStorageImage, DeleteStorageImage
from .values import ServiceStatus, ServiceType
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
        #TODO
        pass
    
    def change_data(self, name: Optional[str]=None, description: Optional[str]=None,
                    status: Optional[ServiceStatus]=None, type: Optional[ServiceType]=None) -> None:
        '''Cambia los datos del servicio de tienda'''
        #TODO
        pass
    
    def add_image(self, base64_image: str) -> None:
        '''Agrega una imagen al servicio de tienda'''
        #TODO
        pass

    def delete_image(self, image: str) -> None:
        '''Elimina una imagen del servicio de tienda'''
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