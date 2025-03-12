from django.test import TestCase
from core.user import AccountStatus, Role
from datetime import date
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
    num_test = 10
    
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
        for _ in range(10):
            user = UserDataFactory.generate_user_sign_up_user_request()
            response = cls.client.post(cls.route, json.dumps(user), content_type='application/json')
            cls.users.append(response.json()['data'])
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('resources/media')
    
    def test_sign_up(self) -> None:
        for _ in range(self.num_test):
            user_data = UserDataFactory.generate_employee_sign_up_employee_request(self.roles)
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
            self.assertEqual(len(data), len(self.users)+1)
    
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
                   
    def _verify_user_data(self, data: Dict[str, Any], user_data: Dict[str, Any]) -> None:
        self.assertEqual(data['status'], AccountStatus.ENABLE.value)
        self.assertEqual(data['created_date'], date.today().isoformat())
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
    

'''class UserAPITest(TestCase):
    route = '/api/user/'
    auth_route = '/api/user/auth/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = cls.client_class()
        for role in DataFactory.user_test_data.get_roles():
            cls.client.post(f'/api/role/?name={role}')
        cls.user_request = DataFactory.generate_sign_up_request()
        cls.user_dto = [cls.client.post(cls.route, user_data).json()['data'] for user_data in cls.user_request]
        
    def test_sign_in(self) -> None:
        for user_data, user in zip(self.user_request, self.user_dto):
            with self.subTest(user_data=user_data):
                response = self.client.post(self.auth_route, {'phone_number': user_data['phone_number'], 'password': user_data['password']})
                data = response.json()['data']
                self.assertEqual(response.status_code, 200)
                self.assertEqual(data, user)
    
    def test_update_user(self) -> None:
        for user, user_data in zip(self.user_dto, DataFactory.generate_update_user_request()):
            with self.subTest(user_data=user_data):
                user_data['id'] = user['id']
                user_data['phone_number'] = user_data['phone_number'][0:5] + str((int(user_data['phone_number'][5])+1)%10) + user_data['phone_number'][6:]
                user_data['email'] = 'test_' + user_data['email']
                response = self.client.put(self.route, user_data, content_type='application/json')
                data = response.json()['data']
                self.assertEqual(data['name'], user_data['name'].lower())
                self.assertEqual(data['phone_number'], user_data['phone_number'].lower())
                self.assertEqual(data['email'], user_data['email'].lower())
    
    def test_update_user_void(self) -> None:
        for user_data in self.user_dto:
            with self.subTest(user_data=user_data):
                response = self.client.put(self.route, {'id': user_data['id']}, content_type='application/json')
                self.assertEqual(response.status_code, 200)
    
    def test_filter_users(self) -> None:
        response = self.client.get(self.route, data={'order_by': 'name'})
        data = response.json()['data']
        expected_data = [user_data['name'].lower() for user_data in self.user_request]
        for user in data:
            self.assertTrue(user['name'] in expected_data)
        self.assertTrue(len(data)==len(self.user_request))
    
    def test_filter_users_query(self) -> None:
        request = {
            'expresion': 'birthdate>1940-01-01 and gender=FEMENINO',
            'order_by': 'name',
            'order_direction': 'ASC',
            'limit': 2,
            'offset': 1
            }
        response = self.client.get(self.route, data=request)
        data = response.json()['data']
        filtered_data = []
        for user in self.user_dto:
            if date.fromisoformat(user['birthdate'])>date(1940, 1, 1) and user['gender']=='FEMENINO':
                filtered_data.append(user)
        expected_data = sorted([user['name'] for user in filtered_data], reverse=True)
        for user in data:
            self.assertTrue(user['name'] in expected_data)
        self.assertTrue(len(data)<=2)

    def test_add_role(self) -> None:
        for user in self.user_dto:
            for role in DataFactory.user_test_data.get_sample_list_roles():
                with self.subTest(user=user, role=role):
                    request = {'user_id': user['id'], 'role': role}
                    response = self.client.post(f'{self.route}role/', request)
                    self.assertEqual(response.status_code, 200)
                    data = response.json()['data']
                    self.assertTrue(role.lower() in [role['name'] for role in data['roles']])

    def test_delete_role(self) -> None:
        for user in self.user_dto:
            for role in DataFactory.user_test_data.get_sample_list_roles():
                with self.subTest(user=user, role=role):
                    response = self.client.delete(f'{self.route}role/?user_id={user["id"]}&role={role}')
                    self.assertEqual(response.status_code, 200)
                    data = response.json()['data']
                    self.assertFalse(role.lower() in [role['name'] for role in data['roles']])
    
    def test_add_not_registered_role(self) -> None:
        for user in self.user_dto:
            for role in DataFactory.user_test_data.get_sample_list_roles():
                with self.subTest(user=user, role=role):
                    response = self.client.post(f'{self.route}role/', {'user_id': user['id'], 'role': role+'_invalid'})
                    self.assertEqual(response.status_code, 400)
                    self.assertEqual(response.json()['error'], 'ModelNotFoundException')'''