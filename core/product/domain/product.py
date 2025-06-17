from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date
from decimal import Decimal
from core.common import ID, Event
from core.common.values import AmountValue
from typing import Optional, List, ClassVar
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted
from core.store_service.domain.values import ServiceType
from .values import ProductName, ProductStatus
from .events import ProductSaved, ProductDeleted
from .exceptions import CannotReduceStockException

class Product(BaseModel):
    id: str
    name: str
    service_type: ServiceType
    service_subtype: str
    product_type: str
    volume: int
    description: str
    price: Decimal
    stock: int
    images: List[str]
    stock_modified_date: date
    created_date: date
    status: ProductStatus
    IMAGE_PATH: ClassVar[str] = f'product'
    _events: List[Event] = PrivateAttr(default=[])
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Product':
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.name = self.name.lower().strip()
        self.description = self.description.lower()
        ID.validate(self.id)
        ProductName.validate(self.name)
        self.set_images(self.images)
    
    def change_data(self, name: Optional[str]=None, service_type: Optional[ServiceType]=None,
                    description: Optional[str]=None, price: Optional[Decimal]=None,
                    additional_stock: int = 0, images: Optional[List[str]]=None,
                    status: Optional[ProductStatus]=None, service_subtype: Optional[str]=None,
                    product_type: Optional[str]=None, volume: Optional[int]=None) -> None:
        if name is not None:
            self.name = name
        if service_type is not None:
            self.service_type = service_type
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if additional_stock > 0:
            self.stock += additional_stock
            self.stock_modified_date = date.today()
        if images is not None:
            self._events.append(ImageDeleted(image_urls=[img for img in self.images if img not in images]))
            self.images = images
        if status is not None:
            self.status = status
        if service_subtype is not None:
            self.service_subtype = service_subtype
        if product_type is not None:
            self.product_type = product_type
        if volume is not None:
            self.volume = volume
        
        self._validate_data()
    
    def reduce_stock(self, quantity: int) -> None:
        AmountValue.validate(quantity)
        if self.stock < quantity:
            raise CannotReduceStockException.cannot_reduce_stock(self.id, self.stock, quantity)
        self.stock -= quantity
        
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
        ProductSaved(product=self).publish()
        for event in self._events:
            event.publish()
    
    def delete(self) -> None:
        ProductDeleted(product=self).publish()


class ProductFactory:
    @classmethod
    def create(cls, name: str, service_type: ServiceType, description: str, price: Decimal,
               stock: int, images: List[str], service_subtype: str, product_type: str, volume: int) -> Product:
        return Product(
            id=ID.generate(),
            name=name,
            service_type=service_type,
            description=description,
            price=price,
            stock=stock,
            images=images,
            created_date=date.today(),
            stock_modified_date=date.today(),
            status=ProductStatus.ENABLE,
            service_subtype=service_subtype,
            product_type=product_type,
            volume=volume
        )
    
    @classmethod
    def load(cls, id: str, name: str, service_type: ServiceType, description: str, price: Decimal,
             stock: int, images: List[str], created_date: date, status: ProductStatus, service_subtype: str,
             product_type: str, volume: int, stock_modified_date: date) -> Product:
        return Product(
            id=id,
            name=name,
            service_type=service_type,
            description=description,
            price=price,
            stock=stock,
            images=images,
            created_date=created_date,
            status=status,
            service_subtype=service_subtype,
            product_type=product_type,
            volume=volume,
            stock_modified_date=stock_modified_date
        )