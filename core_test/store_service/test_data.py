import json
from typing import List, Dict, Any, Optional, Tuple
import random
from core.store_service import StoreServiceFactory, StoreService, ServiceType, ServiceStatus
import lorem

class StoreTestData:
    instance: Optional['StoreTestData'] = None
    
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
    
    @classmethod
    def get_names(self) -> List[str]:
        return self.data['names']
    
    @classmethod
    def get_invalid_names(self) -> List[str]:
        return self.data['invalid_names']
    
    @classmethod
    def get_service_type(self) -> ServiceType:
        return random.choice(list(ServiceType))
    
    @classmethod
    def get_service_status(self) -> ServiceStatus:
        return random.choice(list(ServiceStatus))
    
    @classmethod
    def get_description(self) -> str:
        return lorem.sentence()


class DataFactory:
    store_test_data: StoreTestData = StoreTestData.get_instance()
    
    @classmethod
    def generate_store_services(cls) -> List[StoreService]:
        return [
            StoreServiceFactory.create(
                name=name,
                description=cls.store_test_data.get_description(),
                type=cls.store_test_data.get_service_type()
            )
            for name in cls.store_test_data.get_names()
        ]