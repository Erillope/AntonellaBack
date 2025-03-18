from django.test import TestCase
from datetime import date
from .test_data import UserDataFactory
import json
from core.user import Role
from typing import Dict, Any

class RoleApiTest(TestCase):
    route = '/api/role/'
    num_test = 10
    
    def test_create(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            with self.subTest(request=request):
                response = self.client.post(self.route, json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['created_date'], date.today().isoformat())
                self._validate_role(request, data)
    
    def _validate_role(self, request: Dict[str, Any], data: Dict[str, Any]) -> None:
        self.assertEqual(data['name'], request['name'].lower())
        for request_access in request['accesses']:
            for data_access in data['accesses']:
                if request_access['access'] == data_access['access']:
                    for request_access_permission in request_access['permissions']:
                        self.assertIn(request_access_permission, data_access['permissions'])
        
    def test_create_already_exists(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            with self.subTest(request=request):        
                response = self.client.post(self.route, json.dumps(request), content_type='application/json')
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'RoleAlreadyExistsException')   
    
    def test_create_invalid_role_name(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            request['name'] = Role.MATCHER.generate_invalid(50)
            with self.subTest(request=request):
                response = self.client.post(self.route, json.dumps(request), content_type='application/json')
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'InvalidRoleException')
    
    def test_update(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            update_request = UserDataFactory.generate_create_role_request()
            update_request['role'] = request['name']
            with self.subTest(update_request=update_request):
                response = self.client.put(self.route, json.dumps(update_request), content_type='application/json')
                data = response.json()['data']
                self._validate_role(update_request, data)
    
    def test_rename_already_exists(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            request_2 = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request_2), content_type='application/json')
            update_request = UserDataFactory.generate_create_role_request()
            update_request['role'] = request['name']
            update_request['name'] = request_2['name']
            with self.subTest(update_request=update_request):
                response = self.client.put(self.route, json.dumps(update_request), content_type='application/json')
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'RoleAlreadyExistsException')
    
    def test_invalid_rename(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            update_request = UserDataFactory.generate_create_role_request()
            update_request['role'] = request['name']
            update_request['name'] = Role.MATCHER.generate_invalid(50)
            with self.subTest(update_request=update_request):
                response = self.client.put(self.route, json.dumps(update_request), content_type='application/json')
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'InvalidRoleException')
    
    def test_get_all(self) -> None:
        requests = [UserDataFactory.generate_create_role_request() for _ in range(self.num_test)]
        for request in requests:
            self.client.post(self.route, json.dumps(request), content_type='application/json')
        response = self.client.get(self.route)
        data = response.json()['data']
        self.assertEqual(len(data), len(requests)+1)
    
    def test_delete(self) -> None:
        requests = [UserDataFactory.generate_create_role_request() for _ in range(self.num_test)]
        for request in requests:
            self.client.post(self.route, json.dumps(request), content_type='application/json')
        self.client.delete(self.route+'?role='+request['name'])
        response = self.client.get(self.route)
        data = response.json()['data']
        self.assertEqual(len(data), len(requests))
    
    def test_delete_role_and_user_rol(self) -> None:
        create_role_requests = [UserDataFactory.generate_create_role_request() for _ in range(self.num_test)]
        for role_request in create_role_requests:
            self.client.post(self.route, json.dumps(role_request), content_type='application/json')
            user_request = UserDataFactory.generate_employee_sign_up_employee_request(
                [role['name'] for role in create_role_requests]
            )
            user_request['employee_data']['roles'] = [role_request['name']]
            user = self.client.post('/api/user/', json.dumps(user_request), content_type='application/json').json()['data']
            with self.subTest():
                self.client.delete(self.route+'?role='+role_request['name'])
                self.assertIn(role_request['name'], user_request['employee_data']['roles'])
                user = self.client.get('/api/user/', data={'user_id': user['id']}).json()['data']
                self.assertNotIn(role_request['name'], user.get('roles', []))
    
    def test_get(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_create_role_request()
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            with self.subTest(request=request):
                response = self.client.get(self.route+'?role='+request['name'])
                data = response.json()['data']
                self._validate_role(request, data)