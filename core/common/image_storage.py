from .exceptions import InvalidBase64FormatException, MediaNotFoundException
from .config import MEDIA
from .events import Event, EventSubscriber
import base64
import os
from pydantic import BaseModel, PrivateAttr, model_validator
from core.common import ID
from typing import List

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
    
    @classmethod
    def is_media_url(cls, path: str) -> bool:
        return path.startswith(MEDIA)
    

class ImageSaved(Event):
    '''Evento para cuando una imagen es guardada'''
    def __init__(self, images: List[Base64ImageStorage]):
        self.images = images
    
        
class ImageDeleted(Event):
    '''Evento para cuando una imagen es guardada'''
    def __init__(self, image_urls: List[str]):
        self.image_urls = image_urls
        
        
class Base64SaveStorageImage(EventSubscriber):
    def save(self, image: Base64ImageStorage) -> None:
        """Guarda una imagen en un directorio y retorna la URL"""
        binary_image = self.decode(image.base64_image)
        self.create_if_not_exists(image.get_url())
        with open(image.get_url(), "wb") as file:
            file.write(binary_image)
    
    @classmethod
    def decode(cls, base64_image: str) -> bytes:
        try:
            return base64.b64decode(base64_image)
        except Exception:
            raise InvalidBase64FormatException.invalid_format()
        
    @classmethod
    def create_if_not_exists(cls, path: str) -> None:
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

    def handle(self, event: Event) -> None:
        if isinstance(event, ImageSaved):
            for image in event.images:
                self.save(image)


class DeleteStorageImage(EventSubscriber):
    def delete(self, path: str) -> None:
        if os.path.exists(path) and path.startswith(MEDIA):
            os.remove(path)
            return
        raise MediaNotFoundException.media_not_found(path)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, ImageDeleted):
            for image in event.image_urls:
                self.delete(image)