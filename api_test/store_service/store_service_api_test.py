from django.test import TestCase
from .test_data import DataFactory
from core.store_service import ServiceStatus
from datetime import date

class StoreServiceApiTest(TestCase):
    route = '/api/store_service/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = cls.client_class()
        cls.services_dto = [cls.client(cls.route, request) 
                        for request in DataFactory.generate_create_store_service_requests()]
        
    def test_create_store_service(self) -> None:
        for request in DataFactory.generate_create_store_service_requests():
            with self.subTest():
                response = self.client.post(self.route, request)
                self.assertEqual(response.status_code, 200)
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower())
                self.assertEqual(data['description'], request['description'].lower())
                self.assertEqual(data['status'], ServiceStatus.ENABLE.value)
                self.assertEqual(data['type'], request['type'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['created_date'], date.today().isoformat())