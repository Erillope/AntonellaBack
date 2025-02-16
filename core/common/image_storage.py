from .values import PatternMatcher
from .exceptions import InvalidBase64FormatException, MediaNotFoundException
from .config import MEDIA
from .events import Event, EventSubscriber
import base64
import os
from pydantic import BaseModel, PrivateAttr, model_validator
from core.common import ID

class Base64ImageStorage(BaseModel):
    folder: str
    base64_image: str
    _url: str = PrivateAttr(default='')
    
    @model_validator(mode='after')
    def init(self) -> 'Base64ImageStorage':
        self._url = f'{MEDIA}/{self.folder}/{ID.generate()}.png'
        return self
    
    def get_url(self) -> str:
        return self._url
    

class ImageSaved(Event):
    '''Evento para cuando una imagen es guardada'''
    def __init__(self, image: Base64ImageStorage):
        self.image = image
    
        
class ImageDeleted(Event):
    '''Evento para cuando una imagen es guardada'''
    def __init__(self, image_url: str):
        self.image_url = image_url
        
        
class Base64SaveStorageImage(EventSubscriber):
    URL_REGEX = r'^[A-Za-z0-9+/]+={0,2}$'
    MATCHER = PatternMatcher(pattern=URL_REGEX)
    
    def save(self, image: Base64ImageStorage) -> None:
        """Guarda una imagen en un directorio y retorna la URL"""
        self.verify_base64(image.base64_image)
        binary_image = base64.b64decode(image.base64_image)
        self.create_if_not_exists(image.get_url())
        with open(image.get_url(), "wb") as file:
            file.write(binary_image)

    @classmethod
    def verify_base64(cls, image: str) -> None:
        if not cls.MATCHER.match(image):
            raise InvalidBase64FormatException.invalid_format()
    
    @classmethod
    def create_if_not_exists(cls, path: str) -> None:
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

    def handle(self, event: Event) -> None:
        if isinstance(event, ImageSaved):
            self.save(event.image)


class DeleteStorageImage(EventSubscriber):
    def delete(self, path: str) -> None:
        if os.path.exists(path) and path.startswith(MEDIA):
            os.remove(path)
            return
        raise MediaNotFoundException.media_not_found(path)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, ImageDeleted):
            self.delete(event.image_url)