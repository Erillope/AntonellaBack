import unittest
from core.store_service import StoreServiceFactory
from core.store_service.domain.exceptions import InvalidServiceNameException
from .test_data import DataFactory

class StoreServiceCreationTest(unittest.TestCase):
    def test_store_service_creation(self) -> None:
        for name in DataFactory.store_test_data.get_names():
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            with self.subTest(name=name, description=description, service_type=service_type):
                service = StoreServiceFactory.create(name=name, description=description, type=service_type)
                self.assertEqual(service.name, name.lower())
                self.assertEqual(service.description, description.lower())
                self.assertEqual(service.type, service_type)

    def test_store_service_create_invalid_name(self) -> None:
        for invalid_name in DataFactory.store_test_data.get_invalid_names():
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            with self.subTest(invalid_name=invalid_name, description=description, service_type=service_type):
                with self.assertRaises(InvalidServiceNameException):
                    StoreServiceFactory.create(name=invalid_name, description=description, type=service_type)
    
    def test_change_data(self) -> None:
        for store_service, name in zip(DataFactory.generate_store_services(),
                                       DataFactory.store_test_data.get_names()):
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            status = DataFactory.store_test_data.get_service_status()
            with self.subTest(store_service=store_service, name=name, description=description, 
                              service_type=service_type, status=status):
                store_service.change_data(name=name, description=description, type=service_type, status=status)
                self.assertEqual(store_service.name, name.lower())
                self.assertEqual(store_service.description, description.lower())
                self.assertEqual(store_service.type, service_type)
                self.assertEqual(store_service.status, status)

