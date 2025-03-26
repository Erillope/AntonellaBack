from django.test import TestCase
from .test_data import StoreTestData
from core.store_service import ServiceStatus
import json
import shutil
import os
from core.common.config import MEDIA

class StoreServiceApiTest(TestCase):
    num_test = 10
    route = '/api/store_service/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        if MEDIA == 'resources/media/':
            raise Exception('No se puede correr los test con MEDIA en resources')
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('resources_test/media')
    
    def test_create_store_service(self) -> None:
        for _ in range(self.num_test):
            request = StoreTestData.generate_create_service_request(
                questions=[StoreTestData.generate_create_form_question_request()]
            )
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower().strip())
                self.assertEqual(data['description'], request['description'].lower().strip())
                self.assertEqual(data['type'], request['type'])
                self.assertEqual(data['duration'], request['duration'])
                self.assertEqual(data['prices'], request['prices'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['status'], ServiceStatus.ENABLE.value)
                for image in data['images']:
                    self.assertTrue(os.path.exists(image))
    
    def test_create_store_service_with_invalid_name(self) -> None:
        for _ in range(self.num_test):
            request = StoreTestData.generate_create_service_request(
                questions=[StoreTestData.generate_create_form_question_request()]
            )
            request['name'] = 'xd'
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidServiceNameException')
    
    def test_update_store_service(self) -> None:
        for _ in range(self.num_test):
            request = StoreTestData.generate_create_service_request(
                questions=[StoreTestData.generate_create_form_question_request()]
            )
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            data = response.json()['data']
            request = StoreTestData.generate_update_service_request(data['id'])
            with self.subTest():
                response = self.client.put(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower().strip())
                self.assertEqual(data['description'], request['description'].lower().strip())
                self.assertEqual(data['type'], request['type'])
                self.assertEqual(data['duration'], request['duration'])
                self.assertEqual(data['prices'], request['prices'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['status'], ServiceStatus.ENABLE.value)
                for image in data['images']:
                    self.assertTrue(os.path.exists(image))
    
    def test_delete_store_service(self) -> None:
        for _ in range(self.num_test):
            request = StoreTestData.generate_create_service_request(
                questions=[StoreTestData.generate_create_form_question_request()]
            )
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            data = response.json()['data']
            with self.subTest():
                self.client.delete(f'{self.route}?id={data['id']}')
                response = self.client.get(self.route, data={'id': data['id']})
                self.assertEqual(response.json()['error'], 'ModelNotFoundException')