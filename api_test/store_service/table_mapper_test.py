from django.test import TestCase
from app.store_service.mapper import StoreServiceTableMapper
from core.store_service import ServiceStatus, ServiceType
from .test_data import DataFactory

class StoreServiceTableMapperTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.mapper = StoreServiceTableMapper()
        
    def test_to_store_service(self) -> None:
        for store_service_table in DataFactory.generate_store_service_tables():
            with self.subTest(store_service_table=store_service_table):
                store_service = self.mapper.to_model(store_service_table)
                self.assertEqual(store_service.id, str(store_service_table.id))
                self.assertEqual(store_service.name, store_service_table.name)
                self.assertEqual(store_service.description, store_service_table.description)
                self.assertEqual(store_service.status, ServiceStatus(store_service_table.status))
                self.assertEqual(store_service.type, ServiceType(store_service_table.type))
                self.assertEqual(store_service.created_date, store_service_table.created_date)
    
    def test_to_table(self) -> None:
        for store_service in DataFactory.generate_store_services():
            with self.subTest(store_service=store_service):
                store_service_table = self.mapper.to_table(store_service)
                self.assertEqual(str(store_service_table.id), store_service.id)
                self.assertEqual(store_service_table.name, store_service.name)
                self.assertEqual(store_service_table.description, store_service.description)
                self.assertEqual(store_service_table.status, store_service.status.value)
                self.assertEqual(store_service_table.type, store_service.type.value)
                self.assertEqual(store_service_table.created_date, store_service.created_date)