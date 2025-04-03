from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date, time
from .values import ServiceStatus, ServiceType, ServiceName, Price
from .events import StoreServiceDeleted, StoreServiceSaved
from core.common import ID, Event
from typing import Optional, List, ClassVar
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted

class StoreService(BaseModel):
    "Servicio de tienda"
    id: str
    name: str
    duration: time
    description: str
    prices: List[Price]
    status: ServiceStatus
    type: ServiceType
    subtype: str
    images: List[str]
    created_date: date
    IMAGE_PATH: ClassVar[str] = f'store_service'
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
        self.set_images(self.images)
    
    def change_data(self, name: Optional[str]=None, description: Optional[str]=None,
                    status: Optional[ServiceStatus]=None, type: Optional[ServiceType]=None,
                    duration: Optional[time]=None, images: Optional[List[str]]=None,
                    prices: Optional[List[Price]]=None, subtype: Optional[str]=None) -> None:
        '''Cambia los datos del servicio de tienda'''
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if status is not None:
            self.status = status

        if type is not None:
            self.type = type
            
        if duration is not None:
            self.duration = duration
        
        if images is not None:
            self._events.append(ImageDeleted(image_urls=[img for img in self.images if img not in images]))
            self.images = images
        
        if prices is not None:
            self.prices = prices
        
        if subtype is not None:
            self.subtype = subtype
            
        self._validate_data()
    
    def set_images(self, images: List[str]) -> None:
        self.images = []
        for image in images:
            if Base64ImageStorage.is_media_url(image):
                self.images.append(image)
            else:
                img = Base64ImageStorage(folder=self.IMAGE_PATH, base64_image=image)
                self.images.append(img.get_url())
                self._events.append(ImageSaved(images=[img]))
                
    def save(self) -> None:
        StoreServiceSaved(store_service= self).publish()
        for event in self._events:
            event.publish()
        self._events.clear()
    
    def delete(self) -> None:
        StoreServiceDeleted(store_service = self).publish()


class StoreServiceFactory:
    @staticmethod
    def create(name: str, description: str, type: ServiceType, duration: time, prices: List[Price], images: List[str], subtype: str) -> StoreService:
        return StoreService(
            id = ID.generate(),
            name = name,
            description = description,
            status = ServiceStatus.ENABLE,
            type = type,
            duration = duration,
            prices = prices,
            images= images,
            subtype= subtype,
            created_date = date.today(),
        )
    
    @staticmethod
    def load(id: str, name: str, description: str, status: ServiceStatus, type: ServiceType, duration: time, prices: List[Price], created_date: date, images: List[str], subtype: str) -> StoreService:
        return StoreService(
            id = id,
            name = name,
            description = description,
            status = status,
            type = type,
            duration = duration,
            prices = prices,
            images = images,
            subtype=subtype,
            created_date = created_date,
        )