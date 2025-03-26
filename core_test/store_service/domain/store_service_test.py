import unittest
from core.store_service import StoreServiceFactory
from core.store_service.domain.exceptions import InvalidServiceNameException
from ..test_data import StoreTestData
from datetime import date

class StoreServiceCreationTest(unittest.TestCase):        
    num_tests = 10
    
    def test_create_store_service(self) -> None:
        for _ in range(self.num_tests):
            data = StoreTestData.store_service_data()
            with self.subTest():
                store_service = StoreServiceFactory.create(**data)
                self.assertEqual(store_service.name, data['name'].lower().strip())
                self.assertEqual(store_service.description, data['description'].lower().strip())
                self.assertEqual(store_service.type, data['type'])
                self.assertEqual(store_service.duration, data['duration'])
                self.assertEqual(store_service.prices, data['prices'])
                self.assertEqual(len(store_service.images), len(data['images']))
                self.assertEqual(store_service.created_date, date.today())
    
    def test_create_store_service_with_invalid_name(self) -> None:
        for _ in range(self.num_tests):
            data = StoreTestData.store_service_data()
            data['name'] = 'I'
            with self.subTest():
                with self.assertRaises(InvalidServiceNameException):
                    StoreServiceFactory.create(**data)
    
    def test_change_data(self) -> None:
        for _ in range(self.num_tests):
            store_service = StoreTestData.generate_store_service()
            new_data = StoreTestData.store_service_update_data()
            with self.subTest():
                store_service.change_data(**new_data)
                self.assertEqual(store_service.name, new_data['name'].lower().strip())
                self.assertEqual(store_service.description, new_data['description'].lower().strip())
                self.assertEqual(store_service.type, new_data['type'])
                self.assertEqual(store_service.duration, new_data['duration'])
                self.assertEqual(store_service.prices, new_data['prices'])
                self.assertEqual(len(store_service.images), len(new_data['images']))
                self.assertEqual(store_service.status, new_data['status'])