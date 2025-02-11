from .values import PatternMatcher, ID
from .exceptions import InvalidBase64FormatException, MediaNotFoundException
import base64
import os

class Base64SaveStorageImage:
    URL_REGEX = r'^data:image\/(png|jpeg|jpg|gif|bmp|webp);base64,[A-Za-z0-9+/]+={0,2}$'
    MATCHER = PatternMatcher(pattern=URL_REGEX)
    BASE = "resources/media"
    
    def __init__(self, folder_name: str) -> None:
        self.folder_name = folder_name
        
    def save(self, image: str) -> str:
        self.verify_base64(image)
        binary_image = base64.b64decode(image.split(",")[1])
        image_url = f'{self.BASE}/{self.folder_name}/{ID.generate()}.png'
        directory = os.path.dirname(image_url)
        os.makedirs(directory, exist_ok=True)
        self._create_if_not_exists(image_url, binary_image)
        return image_url
    
    def _create_if_not_exists(self, path: str, binary_data: bytes) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path, "wb") as file:
            file.write(binary_data)
        
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
        raise MediaNotFoundException.media_not_found(path)