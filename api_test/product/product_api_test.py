from django.test import TestCase
from .test_data import ProductTestData
import json
import shutil
import os
from core.common.config import MEDIA

class ProductApiTest(TestCase):
    num_test = 10
    route = '/api/product/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        if MEDIA == 'resources/media/':
            raise Exception('No se puede correr los test con MEDIA en resources')
        cls.client = cls.client_class()
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('resources_test/media')
    
    def test_create_product(self) -> None:
        for _ in range(self.num_test):
            request = ProductTestData.generate_create_product_request()
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower().strip())
                self.assertEqual(data['description'], request['description'].lower().strip())
                self.assertEqual(data['price'], request['price'])
                self.assertEqual(data['stock'], request['stock'])
                self.assertEqual(data['service_type'], request['service_type'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['service_subtype'], request['service_subtype'])
                self.assertEqual(data['product_type'], request['product_type'])
                self.assertEqual(data['volume'], request['volume'])
                for image in data['images']:
                    self.assertTrue(os.path.exists(image))
    
    def test_update_product(self) -> None:
        for _ in range(self.num_test):
            request = ProductTestData.generate_create_product_request()
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            data = response.json()['data']
            stock = data['stock']
            request = ProductTestData.generate_update_product_request(data['id'])
            with self.subTest():
                response = self.client.put(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower().strip())
                self.assertEqual(data['description'], request['description'].lower().strip())
                self.assertEqual(data['price'], request['price'])
                self.assertEqual(data['stock'], request['additional_stock'] + stock)
                self.assertEqual(data['service_type'], request['service_type'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['service_subtype'], request['service_subtype'])
                self.assertEqual(data['product_type'], request['product_type'])
                self.assertEqual(data['volume'], request['volume'])
                for image in data['images']:
                    self.assertTrue(os.path.exists(image))
    
    
    def test_delete_product(self) -> None:
        for _ in range(self.num_test):
            request = ProductTestData.generate_create_product_request()
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            data = response.json()['data']
            with self.subTest():
                self.client.delete(self.route+'?id='+data['id'])
                response = self.client.get(self.route, data={'id': data['id']})
                self.assertEqual(response.json()['error'], 'ModelNotFoundException')
                