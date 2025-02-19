from core_test.store_service.test_data import DataFactory as CoreDataFactory
from core.common import ID
from app.store_service.models import StoreServiceTableData
from typing import List, Dict, Any
from datetime import date
import random

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
                'images': cls.store_test_data.get_sample_base64_images(),
                'questions': [cls.generate_create_question_request() for _ in range(3)]
            }
            for name in cls.store_test_data.get_names()
        ]
    
    @classmethod
    def generate_create_question_request(cls) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'title': cls.store_test_data.get_description(),
            'input_type': 'CHOICE',
        }
        if data['input_type'] == 'CHOICE':
            data['choice_type'] = random.choice(['TEXT', 'IMAGE'])
            if data['choice_type'] == 'TEXT':
                data['choices'] = [cls.store_test_data.get_description() for _ in range(3)]
            if data['choice_type'] == 'IMAGE':
                data['choices'] = [
                    {
                        'image': image,
                        'option': cls.store_test_data.get_description()
                    }
                    for image in cls.store_test_data.get_sample_base64_images()
                ]
        return data