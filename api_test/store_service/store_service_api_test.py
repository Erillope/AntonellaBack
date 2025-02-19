from django.test import TestCase
from .test_data import DataFactory
from core.store_service import ServiceStatus
from datetime import date
import json
from typing import Dict, Any, List
import shutil
import os

class StoreServiceApiTest(TestCase):
    route = '/api/store_service/'
    image_route = '/api/store_service/image/'
    question_route = '/api/store_service/question/'
    choice_route = '/api/store_service/question/choice/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = cls.client_class()
        requests = DataFactory.generate_create_store_service_requests()
        cls.services_dto = []
        for request in requests:
            response = cls.client.post(cls.route, json.dumps(request), content_type='application/json')
            data = response.json()['data']
            cls.services_dto.append(data)
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('resources/media')
    
    def test_create_store_service(self) -> None:
        for request in DataFactory.generate_create_store_service_requests():
            with self.subTest():
                response = self.client.post(self.route, json.dumps(request), content_type='application/json')
                self.assertEqual(response.status_code, 200)
                data = response.json()['data']
                self.assertEqual(data['name'], request['name'].lower())
                self.assertEqual(data['description'], request['description'].lower())
                self.assertEqual(data['status'], ServiceStatus.ENABLE.value)
                self.assertEqual(data['type'], request['type'])
                self.assertEqual(len(data['images']), len(request['images']))
                self.assertEqual(data['created_date'], date.today().isoformat())
                self.assertEqual(len(data['questions']), len(request['questions']))
                self._verify_service_images(data['images'])
                for i in range(len(data['questions'])):
                    self._verify_question(request['questions'][i], data['questions'][i])
    
    def _verify_question(self, question: Dict[str, Any], data: Dict[str, Any]) -> None:
        self.assertEqual(data['title'], question['title'].lower())
        self.assertEqual(data['input_type'], question['input_type'])
        if data['input_type'] == 'CHOICE':
            self.assertEqual(data['choice_type'], question['choice_type'])
            self.assertEqual(len(data['choices']), len(question['choices']))
            if data['choice_type'] == 'TEXT':
                self.assertEqual(data['choices'], question['choices'])
            else:
                self.assertEqual([choice['option'] for choice in data['choices']], [choice['option'] for choice in question['choices']])
                self._verify_choice_images([choice['image'] for choice in data['choices']])
    
    def _verify_service_images(self, images: List[str]) -> None:
        for image in images:
            self.assertIn(image.split('/')[-1], os.listdir('resources/media/store_service'))
    
    def _verify_choice_images(self, images: List[str]) -> None:
        for image in images:
            self.assertIn(image.split('/')[-1], os.listdir('resources/media/choices'))
    
    def _verify_not_in_service_images(self, image: str) -> None:
        self.assertNotIn(image.split('/')[-1], os.listdir('resources/media/store_service'))
    
    def _verify_not_in_choice_images(self, image: str) -> None:
        self.assertNotIn(image.split('/')[-1], os.listdir('resources/media/choices'))
        
    def test_find_store_service(self) -> None:
        for service in self.services_dto:
            with self.subTest():
                response = self.client.get(self.route + "?id=" + service['id'])
                self.assertEqual(response.status_code, 200)
                data = response.json()['data']
                self.assertEqual(data, service)

    def test_delete_store_service(self) -> None:
        for request in DataFactory.generate_create_store_service_requests()[0:1]:
            with self.subTest():
                service = self.client.post(self.route, json.dumps(request), content_type='application/json').json()['data']
                response = self.client.delete(self.route + "?id=" + service['id'])
                deleted_service = self.client.get(self.route + "?id=" + service['id'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(deleted_service.json()['error'], 'ModelNotFoundException')
                for image in service['images']:
                    self._verify_not_in_service_images(image)
    
    def test_update_store_service(self) -> None:
        for service in self.services_dto:
            with self.subTest():
                new_type = DataFactory.store_test_data.get_service_type().value
                status = DataFactory.store_test_data.get_service_status().value
                request = {'id': service['id'], 'name': 'newName', 'description': 'new description',
                           'type': new_type, 'status': status}
                response = self.client.put(self.route, json.dumps(request), content_type='application/json')
                updated_service = response.json()['data']
                self.assertEqual(response.status_code, 200)
                self.assertEqual(updated_service['name'], request['name'].lower())
                self.assertEqual(updated_service['description'], request['description'].lower())
                self.assertEqual(updated_service['status'], status)
                self.assertEqual(updated_service['type'], new_type)
    
    def test_add_image_to_store_service(self) -> None:
        for service in self.services_dto:
            with self.subTest():
                request = {'service_id': service['id'],
                           'base64_image': DataFactory.store_test_data.get_sample_base64_images()[0]}
                response = self.client.post(self.image_route, json.dumps(request), content_type='application/json')
                updated_service = response.json()['data']
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(updated_service['images']), len(service['images']) + 1)
                self._verify_service_images(updated_service['images'])
    
    def test_delete_image_from_store_service(self) -> None:
        for service in self.services_dto:
            with self.subTest():
                response = self.client.delete(self.image_route+"?service_id="+service['id']+"&image="+service['images'][0])
                service_data = response.json()['data']
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(service_data['images']), len(service['images']) - 1)
                self._verify_not_in_service_images(service['images'][0])
    
    def test_add_question(self) -> None:
        for service in self.services_dto:
            request = DataFactory.generate_create_question_request()
            with self.subTest():
                request['service_id'] = service['id']
                response = self.client.post(self.question_route, json.dumps(request), 
                                            content_type='application/json')
                self.assertEqual(response.status_code, 200)
                data = response.json()['data']
                self._verify_question(request, data)
                updated_service = self.client.get(self.route+'?id='+service['id'])
                updated_service_data = updated_service.json()['data']
                self.assertEqual(len(updated_service_data['questions']), len(service['questions'])+1)
    
    def test_delete_question(self) -> None:
        for service in self.services_dto:
            with self.subTest():
                response = self.client.delete(self.question_route+"?id="+service['questions'][0]['id'])
                deleted_question = response.json()['data']
                updated_service = self.client.get(self.route+'?id='+service['id']).json()['data']
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(updated_service['questions']), len(service['questions'])-1)
                self.assertNotIn(deleted_question['id'], [question['id'] for question in updated_service['questions']])
                if deleted_question['input_type'] == 'CHOICE' and deleted_question['choice_type'] == 'IMAGE':
                    for choice in deleted_question['choices']:
                        self._verify_not_in_choice_images(choice['image'])
    
    def test_find_question(self) -> None:
        for service in self.services_dto:
            for question in service['questions']:
                with self.subTest():
                    response = self.client.get(self.question_route+"?id="+question['id'])
                    data = response.json()['data']
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(data, question)

    def test_update_question(self) -> None:
        for service in self.services_dto:
            for question in service['questions']:
                with self.subTest():
                    new_title = 'new title' + question['id']
                    request = {'id': question['id'], 'title': new_title}
                    response = self.client.put(self.question_route, json.dumps(request), content_type='application/json')
                    updated_question = response.json()['data']
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(updated_question['title'], new_title.lower())