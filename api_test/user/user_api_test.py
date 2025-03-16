from django.test import TestCase
from core.user import Role
from core_test.images_data import get_base64_string
from .test_data import UserDataFactory
import json
import os
from core.common.config import MEDIA
import shutil
from typing import Dict, Any
from core.common.config import AppConfig
from core.user.domain.values import UserPassword, UserPhoneNumber, UserEmail
import random

class UserAPITest(TestCase):
    route = '/api/user/'
    auth_route = '/api/user/auth/'
    num_test = 1
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = cls.client_class()
        cls.roles = [Role.MATCHER.generate() for _ in range(10)]
        for role in cls.roles:
            request = UserDataFactory.generate_create_role_request()
            request['name'] = role
            cls.client.post(f'/api/role/', json.dumps(request), content_type='application/json')
        cls.users = []
        cls.employees = []
        for _ in range(10):
            user = UserDataFactory.generate_user_sign_up_user_request()
            response = cls.client.post(cls.route, json.dumps(user), content_type='application/json')
            cls.users.append(response.json()['data'])
            employee = UserDataFactory.generate_employee_sign_up_employee_request(cls.roles)
            response = cls.client.post(cls.route, json.dumps(employee), content_type='application/json')
            cls.employees.append(response.json()['data'])
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('resources/media')
    
    
    def test_sign_up(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                data = response.json()['data']
                self._verify_user_data(data, user_data)
    
    def test_employee_sign_up(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_employee_sign_up_employee_request(self.roles)
            with self.subTest():
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                data = response.json()['data']
                self._verify_employee_data(data, user_data)
                
    def test_sign_up_other_super_admin(self) -> None:
        admin_data = UserDataFactory.generate_employee_sign_up_employee_request(self.roles)
        admin_data['employee_data']['roles'] += [Role.SUPER_ADMIN]
        response = self.client.post(self.route, json.dumps(admin_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'AlreadyExistsSuperAdminException')
    
    def test_sign_in_super_admin(self) -> None:
        admin_data = AppConfig.default_super_admin()
        response = self.client.post(self.auth_route, json.dumps({'phone_number': admin_data['phone_number'], 'password': admin_data['password']}), content_type='application/json')
        data = response.json()['data']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['roles'], [Role.SUPER_ADMIN.lower()])
    
    def test_sign_in_not_registered_phone_number(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_employee_sign_up_employee_request(self.roles)
            with self.subTest(user_data=user_data):
                response = self.client.post(self.auth_route, json.dumps({'phone_number': user_data['phone_number']+'1', 'password': user_data['password']}), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'ModelNotFoundException')
    
    def test_sign_in_admin_incorrect_password(self) -> None:
        admin_data = AppConfig.default_super_admin()
        response = self.client.post(self.auth_route, json.dumps({'phone_number': admin_data['phone_number'], 'password': admin_data['password']+'1'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'IncorrectPasswordException')
    
    def test_sign_up_user(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                data = response.json()['data']
                self._verify_user_data(data, user_data)
    
    def test_sign_up_already_exists_user(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            self.client.post(self.route, json.dumps(user_data), content_type='application/json')
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'UserAlreadyExistsException')
    
    def test_sign_up_invalid_phone_number(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['phone_number'] = UserPhoneNumber.MATCHER.generate_invalid(random.randint(1,10))
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidPhoneNumberException')
    
    def test_sign_up_invalid_email(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['email'] = UserEmail.MATCHER.generate_invalid(random.randint(1,20))
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserEmailException')
    
    def test_sign_up_invalid_password(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['password'] = UserPassword.MATCHER.generate_invalid(random.randint(1,20))
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserPasswordException')
    
    def test_sign_up_invalid_name(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['name'] = 'invalid name'
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserNameException')
    
    def test_sign_up_invalid_birthdate(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['birthdate'] = UserDataFactory.get_invalid_birthdate().isoformat()
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserBirthdateException')
    
    def test_sign_up_already_exists_email(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_user_sign_up_user_request()
            user_data['phone_number'] = UserPhoneNumber.MATCHER.generate()
            self.client.post(self.route, json.dumps(user_data), content_type='application/json')
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, json.dumps(user_data), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'UserAlreadyExistsException')
    
    def test_get_user(self) -> None:
        for user in self.users:
            with self.subTest(user=user):
                response = self.client.get(self.route, data={'user_id': user['id']})
                data = response.json()['data']
                self.assertEqual(data['id'], user['id'])
    
    def test_get_user_not_registered(self) -> None:
        for _ in range(self.num_test):
            user = UserDataFactory.generate_user_account()
            response = self.client.get(self.route, data={'user_id': user.id})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['error'], 'ModelNotFoundException')
    
    def test_filter_users(self) -> None:
        request = {
                'order_by': 'name',
                'order_direction': 'ASC',
        }
        with self.subTest(request=request):
            response = self.client.get(self.route+"filter/", data=request)
            data = response.json()['data']
            users_id = [user['id'] for user in data]
            for user in self.users:
                self.assertIn(user['id'], users_id)
            self.assertEqual(len(data), len(self.users)+len(self.employees)+1)
    
    def test_update_user(self) -> None:
        for user in self.users[0:1]:
            user_data = UserDataFactory.generate_user_account()
            request = {
                'id': user['id'],
                'phone_number': user_data.phone_number,
                'email': user_data.email,
                'name': user_data.name,
            }
            with self.subTest(user=user, user_data=user_data):
                response = self.client.put(self.route, json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['phone_number'], user_data.phone_number)
                self.assertEqual(data['email'], user_data.email)
                self.assertEqual(data['name'], user_data.name)
    
    def test_update_employee(self) -> None:
        for employee in self.employees[0:1]:
            employee_data = UserDataFactory.generate_employee_account()
            request = {
                'id': employee['id'],
                'phone_number': employee_data.phone_number,
                'email': employee_data.email,
                'name': employee_data.name,
                'dni': employee_data.dni,
                'address': employee_data.address,
                'photo': get_base64_string(),
                'roles': random.sample(self.roles, k=random.randint(1, len(self.roles)))
            }
            with self.subTest(employee=employee, request=request):
                response = self.client.put(self.route, json.dumps(request), content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['phone_number'], employee_data.phone_number)
                self.assertEqual(data['email'], employee_data.email)
                self.assertEqual(data['name'], employee_data.name)
                self.assertEqual(data['dni'], employee_data.dni)
                self.assertEqual(data['address'], employee_data.address)
                self.assertEqual(data['roles'], [role.lower() for role in request['roles']])
    
    def test_create_employee_already_exists_dni(self) -> None:
        for _ in range(self.num_test):
            request = UserDataFactory.generate_employee_sign_up_employee_request(self.roles)
            self.client.post(self.route, json.dumps(request), content_type='application/json')
            request['phone_number'] = UserPhoneNumber.MATCHER.generate()
            request['email'] = UserEmail.MATCHER.generate()
            with self.subTest():
                response = self.client.post(self.route, json.dumps(request), content_type='application/json')
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'UserAlreadyExistsException')
        
    def _verify_user_data(self, data: Dict[str, Any], user_data: Dict[str, Any]) -> None:
        self.assertEqual(data['email'], user_data['email'].lower())
        self.assertEqual(data['name'], user_data['name'].lower())
        self.assertEqual(data['phone_number'], user_data['phone_number'])
        self.assertEqual(data['gender'], user_data['gender'])
        self.assertEqual(data['birthdate'], user_data['birthdate'])
    
    def _verify_employee_data(self, data: Dict[str, Any], user_data: Dict[str, Any]) -> None:
        self._verify_user_data(data, user_data)
        self.assertEqual(data['dni'], user_data['employee_data']['dni'])
        self.assertEqual(data['address'], user_data['employee_data']['address'])
        self.assertIn(data['photo'].split('/')[-1], os.listdir(MEDIA+'/employee'))
        self.assertEqual(data['roles'], user_data['employee_data']['roles'])