from enum import Enum
from core.common import PatternMatcher
from .exceptions import InvalidServiceNameException
from core.common.image_storage import Base64SaveStorageImage, DeleteStorageImage
from typing import Optional, ClassVar
from pydantic import BaseModel

class ServiceType(Enum):
    HAIR = "CABELLO"
    SPA = "SPA"
    NAIL = "UÑAS"
    MAKEUP = "MAQUILLAJE"


class ServiceStatus(Enum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    

class InputType(Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"

    
class Choice(BaseModel):
    option: str
    image: Optional[str] = None
    IMAGES_FOLDER: ClassVar[str] = 'choices_images'
    IMAGE_CONVERTER: ClassVar[Base64SaveStorageImage] = Base64SaveStorageImage(IMAGES_FOLDER)
    IMAGE_DELETER: ClassVar[DeleteStorageImage] = DeleteStorageImage(IMAGES_FOLDER)
    
    def save_image(self) -> None:
        if self.image:
            self.image = self.IMAGE_CONVERTER.save(self.image)
    
    def delete_image(self) -> None:
        if self.image:
            self.IMAGE_DELETER.delete(self.image)

class ServiceName:
    REGREX = r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÜüÑñ' &-]{3,50}$"
    MATCHER = PatternMatcher(pattern=REGREX)
    
    @classmethod
    def validate(cls, value: str) -> None:
        if not cls.MATCHER.match(value):
            raise InvalidServiceNameException.invalid_service_name(value)