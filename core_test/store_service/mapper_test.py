import unittest
from core.store_service.service.mapper import StoreServiceMapper
from .test_data import DataFactory

class StoreServiceMapperTest(unittest.TestCase):
    def test_to_store_service(self) -> None:
        for create_store_service_dto in DataFactory.generate_create_store_services_dto():
            with self.subTest():
                store_service = StoreServiceMapper.to_store_service(create_store_service_dto)
                self.assertEqual(create_store_service_dto.name.lower(), store_service.name)
                self.assertEqual(create_store_service_dto.description.lower(), store_service.description)
                self.assertEqual(create_store_service_dto.type, store_service.type)
        
    def test_to_dto(self) -> None:
        for store_service in DataFactory.generate_store_services():
            with self.subTest(store_service=store_service):
                dto = StoreServiceMapper.to_dto(store_service)
                self.assertEqual(store_service.id, dto.id)
                self.assertEqual(store_service.name, dto.name.lower())
                self.assertEqual(store_service.description, dto.description.lower())
                self.assertEqual(store_service.type, dto.type)
                self.assertEqual(store_service.created_date, dto.created_date)
                self.assertEqual(store_service.status, dto.status)
                self.assertEqual(store_service.images, dto.images)