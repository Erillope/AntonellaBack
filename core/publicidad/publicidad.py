from pydantic import BaseModel, model_validator, PrivateAttr
from typing import List, Optional, ClassVar
from core.common import ID, Event
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted
from .events import PublicidadSaved, PublicidadDeleted
from datetime import date
from decimal import Decimal
from enum import Enum

class ItemType(str, Enum):
    DISCOUNT = 'descuento'
    FIXED = 'fijo'

class ItemData(BaseModel):
    id: str
    type: ItemType
    fixed_amount: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    
class Publicidad(BaseModel):
    id: str
    service_items: List[ItemData]
    product_items: List[ItemData]
    title: str
    images: list[str]
    description: str
    created_date: date
    enabled: bool = True
    IMAGE_PATH: ClassVar[str] = f'publicidad'
    _events: List[Event] = PrivateAttr(default=[])

    @model_validator(mode='after')
    def validate_data(self) -> 'Publicidad':
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        self.title = self.title.strip()
        self.description = self.description.strip()
        self.set_images(self.images)
    
    def change_data(self, title: Optional[str] = None, images: Optional[List[str]] = None,
                    service_items: Optional[List[ItemData]] = None, product_items: Optional[List[ItemData]] = None,
                    description: Optional[str] = None, enabled: Optional[bool] = None) -> None:
        if title is not None:
            self.title = title
        if images is not None:
            self._events.append(ImageDeleted(image_urls=[img for img in self.images if img not in images]))
            self.images = images
        if service_items is not None:
            self.service_items = service_items
        if product_items is not None:
            self.product_items = product_items
        if description is not None:
            self.description = description
        if enabled is not None:
            self.enabled = enabled
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
        PublicidadSaved(publicidad=self).publish()
        for event in self._events:
            event.publish()
    
    def delete(self) -> None:
        PublicidadDeleted(publicidad=self).publish()


class PublicidadFactory:
    @classmethod
    def create(cls, title: str, images: List[str], description: str, service_items: List[ItemData], product_items: List[ItemData]) -> Publicidad:
        publicidad = Publicidad(
            id=ID.generate(),
            service_items=service_items,
            product_items=product_items,
            title=title,
            images=images,
            description=description,
            created_date=date.today(),
            enabled=True
        )
        return publicidad

    @classmethod
    def load(cls, id: str, title: str, images: List[str], service_items: List[ItemData], product_items: List[ItemData], 
             created_date: date, description: str, enabled: bool) -> Publicidad:
        return Publicidad(
            id=id,
            service_items=service_items,
            product_items=product_items,
            title=title,
            images=images,
            created_date=created_date,
            description=description,
            enabled=enabled
        )