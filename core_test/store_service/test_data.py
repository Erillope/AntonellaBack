import json
from typing import List, Dict, Any, Optional, Tuple
import random
from core.store_service import StoreServiceFactory, StoreService, ServiceType, ServiceStatus
from core_test.images_data import get_base64_strings
import lorem

class StoreTestData:
    instance: Optional['StoreTestData'] = None
    BASE64_IMAGES = get_base64_strings()
    
    def __init__(self) -> None:
        self.data: Dict[str, List[Any]] = {}
        with open('core_test/store_service/store_service_test_data.json') as file:
            self.data = json.load(file)
        self.shuffle()
    
    def shuffle(self) -> None:
        for key in self.data:
            random.shuffle(self.data[key])
    
    @classmethod      
    def get_instance(cls) -> 'StoreTestData':
        if cls.instance is None:
            cls.instance = StoreTestData()
        return cls.instance
    
    def get_names(self) -> List[str]:
        return self.data['names']
    
    def get_invalid_names(self) -> List[str]:
        return self.data['invalid_names']
    
    def get_service_type(self) -> ServiceType:
        return random.choice(list(ServiceType))
    
    def get_service_status(self) -> ServiceStatus:
        return random.choice(list(ServiceStatus))
    
    def get_description(self) -> str:
        return lorem.sentence()
    
    def get_sample_base64_images(self) -> List[str]:
        return random.sample(self.BASE64_IMAGES, random.randint(1, len(self.BASE64_IMAGES)))


class DataFactory:
    store_test_data: StoreTestData = StoreTestData.get_instance()
    
    @classmethod
    def generate_store_services(cls) -> List[StoreService]:
        return [
            StoreServiceFactory.create(
                name=name,
                description=cls.store_test_data.get_description(),
                type=cls.store_test_data.get_service_type(),
                images=cls.store_test_data.get_sample_base64_images()
            )
            for name in cls.store_test_data.get_names()
        ]