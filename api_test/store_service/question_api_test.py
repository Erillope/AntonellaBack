from django.test import TestCase
from .test_data import StoreTestData
from core_test.images_data import get_base64_string
import json
import shutil
import os
from core.common.config import MEDIA

class QuestionApiTest(TestCase):
    num_test = 10
    route = '/api/store_service/question/'
    service_route = '/api/store_service/'

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        if MEDIA == 'resources/media/':
            raise Exception('No se puede correr los test con MEDIA en resources')
        cls.client = cls.client_class()
        cls.services = []
        for _ in range(1):
            request = StoreTestData.generate_create_service_request([StoreTestData.generate_create_form_question_request()])
            response = cls.client.post(cls.service_route, data=json.dumps(request), content_type='application/json')
            cls.services.append(response.json()['data'])

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists('resources_test/media'):
            shutil.rmtree('resources_test/media')

    def test_create_form_question(self) -> None:
        for service in self.services:
            request = StoreTestData.generate_create_form_question_request(service_id=service['id'])
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['title'], request['title'].lower().strip())
                self.assertEqual(data['input_type'], request['input_type'])
    
    def test_create_text_choice_question(self) -> None:
        for service in self.services:
            request = StoreTestData.generate_create_text_choice_question_request(service_id=service['id'])
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['title'], request['title'].lower().strip())
                self.assertEqual(data['input_type'], 'CHOICE')
                self.assertEqual(data['choice_type'], 'TEXT')
                self.assertEqual(data['choices'], [choice for choice in request['choices']])

    def test_create_image_choice_question(self) -> None:
        for service in self.services:
            request = StoreTestData.generate_create_image_choice_question_request(service_id=service['id'])
            with self.subTest():
                response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['title'], request['title'].lower().strip())
                self.assertEqual(data['input_type'], 'CHOICE')
                self.assertEqual(data['choice_type'], 'IMAGE')
                self.assertEqual([choice['option'] for choice in data['choices']],
                                 [choice['option'] for choice in request['choices']])
                for choice in data['choices']:
                    self.assertTrue(os.path.exists(choice['image']))
    
    def test_change_question_title(self) -> None:
        for service in self.services:
            request = StoreTestData.generate_create_form_question_request(service_id=service['id'])
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            question = response.json()['data']
            request = {
                'id': question['id'],
                'title': 'new title'
            }
            with self.subTest():
                response = self.client.put(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['title'], request['title'].lower().strip())
    
    def test_change_question_text_choice(self) -> None:
        for service in self.services[0:1]:
            request = StoreTestData.generate_create_text_choice_question_request(service_id=service['id'])
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            question = response.json()['data']
            request = {
                'id': question['id'],
                'choices': [
                        {
                        'option': f'option{i}'
                    } for i in range(3)
                ]
            }
            with self.subTest():
                response = self.client.put(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['choices'], [choice['option'] for choice in request['choices']])
    
    def test_change_question_image_choice(self) -> None:
        for service in self.services[0:1]:
            request = StoreTestData.generate_create_image_choice_question_request(service_id=service['id'])
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            question = response.json()['data']
            request = {
                'id': question['id'],
                'choices': [
                    {
                        'option': f'option{i}',
                        'image': get_base64_string()
                    } for i in range(3)
                ]
            }
            with self.subTest():
                response = self.client.put(self.route, data=json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual([choice['option'] for choice in data['choices']], 
                                 [choice['option'] for choice in request['choices']])
                for choice in data['choices']:
                    self.assertTrue(os.path.exists(choice['image']))
    
    def test_delete_question(self) -> None:
        for service in self.services:
            request = StoreTestData.generate_create_form_question_request(service_id=service['id'])
            response = self.client.post(self.route, data=json.dumps(request), content_type='application/json')
            question = response.json()['data']
            with self.subTest():
                self.client.delete(self.route+f'?id={question['id']}', data=json.dumps({'id': question['id']}), content_type='application/json')
                response = self.client.get(self.route, data={'id': question['id']})
                self.assertEqual(response.json()['error'], 'ModelNotFoundException')