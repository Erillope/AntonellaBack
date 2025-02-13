from .values import PatternMatcher, ID
from .exceptions import InvalidBase64FormatException, MediaNotFoundException
import base64
import os

class Base64SaveStorageImage:
    URL_REGEX = r'^[A-Za-z0-9+/]+={0,2}$'
    MATCHER = PatternMatcher(pattern=URL_REGEX)
    BASE = "resources/media"
    
    def __init__(self, folder_name: str) -> None:
        self.folder_name = folder_name
        self.folder_url = f'{self.BASE}/{folder_name}'
        if not os.path.exists(self.folder_url):
            os.makedirs(self.folder_url)
        
    def save(self, image: str) -> str:
        """Guarda una imagen en un directorio y retorna la URL"""
        Base64SaveStorageImage.verify_base64(image)
        binary_image = base64.b64decode(image)
        image_url = f'{self.folder_url}/{ID.generate()}.png'
        directory = os.path.dirname(image_url)
        os.makedirs(directory, exist_ok=True)
        with open(image_url, "wb") as file:
            file.write(binary_image)
        return image_url


    @classmethod
    def verify_base64(cls, image: str) -> None:
        if not cls.MATCHER.match(image):
            raise InvalidBase64FormatException.invalid_format()


class DeleteStorageImage:
    BASE = "resources/media"
    def __init__(self, folder_name: str) -> None:
        self.folder_name = folder_name
        
    def delete(self, path: str) -> None:
        folder_path = f'{self.BASE}/{self.folder_name}'
        if os.path.exists(path) and path.startswith(folder_path):
            os.remove(path)
            return
        raise MediaNotFoundException.media_not_found(path)