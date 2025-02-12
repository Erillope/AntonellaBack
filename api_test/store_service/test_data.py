from core_test.store_service.test_data import DataFactory as CoreDataFactory
from core.common import ID
from app.store_service.models import StoreServiceTableData
from typing import List, Dict, Any
from datetime import date

class DataFactory(CoreDataFactory):
    @classmethod
    def generate_store_service_tables(cls) -> List[StoreServiceTableData]:
        return [
            StoreServiceTableData(
                id=ID.generate(),
                name=name.lower(),
                description=cls.store_test_data.get_description().lower(),
                status=cls.store_test_data.get_service_status().value,
                type=cls.store_test_data.get_service_type().value,
                created_date=date.today()
            )
            for name in cls.store_test_data.get_names()
        ]
    
    @classmethod
    def generate_create_store_service_requests(cls) -> List[Dict[str, Any]]:
        return [
            {
                'name': name,
                'description': cls.store_test_data.get_description(),
                'status': cls.store_test_data.get_service_status().value,
                'type': cls.store_test_data.get_service_type().value,
                'images': cls.store_test_data.get_sample_base64_images()
            }
            for name in cls.store_test_data.get_names()
        ]