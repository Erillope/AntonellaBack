from django.test import TestCase
from core.common import ID
from core.user import AccountStatus
from datetime import date
from .test_data import DataFactory

class SignUpUserAPITest(TestCase):
    route = '/api/user/'
    auth_route = '/api/user/auth/'
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = cls.client_class()
        for role in DataFactory.user_test_data.get_roles():
            cls.client.post(f'/api/role/?name={role}')

    def test_sign_up(self) -> None:
        for user_data in DataFactory.generate_sign_up_request()[0:1]:
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, user_data)
                data = response.json()['data']
                ID.validate(data['id'])
                for role in data['roles']:
                    ID.validate(role['id'])
                    date.fromisoformat(role['created_date'])
                self.assertEqual(data['status'], AccountStatus.ENABLE.value)
                self.assertEqual(data['created_date'], date.today().isoformat())
                self.assertEqual(data['email'], user_data['email'].lower())
                self.assertEqual(data['name'], user_data['name'].lower())
                self.assertEqual([role['name'] for role in data['roles']], [role.lower() for role in user_data['roles']])
                self.assertEqual(data['phone_number'], user_data['phone_number'])
                self.assertEqual(data['gender'], user_data['gender'])
                self.assertEqual(data['birthdate'], user_data['birthdate'])
    
    def test_sign_up_email_already_exists(self) -> None:
        for user_data in DataFactory.generate_sign_up_request():
            with self.subTest(user_data=user_data):
                self.client.post(self.route, user_data)
                user_data['phone_number'] = user_data['phone_number'][0:5] + str((int(user_data['phone_number'][5])+1)%10) + user_data['phone_number'][6:]
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'AlreadyExistsUserException')
    
    def test_sign_up_phone_number_already_exists(self) -> None:
        for user_data in DataFactory.generate_sign_up_request():
            with self.subTest(user_data=user_data):
                self.client.post(self.route, user_data)
                user_data['email'] = 'test_' + user_data['email']
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'AlreadyExistsUserException')
    
    def test_sign_up_invalid_phone_number(self) -> None:
        for user_data, invalid_phone_number in zip(DataFactory.generate_sign_up_request(),
                                                    DataFactory.user_test_data.get_invalid_phone_numbers()):
            with self.subTest(user_data=user_data):
                user_data['phone_number'] = invalid_phone_number
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidPhoneNumberException')
    
    def test_sign_up_invalid_email(self) -> None:
        for user_data, invalid_email in zip(DataFactory.generate_sign_up_request(),
                                            DataFactory.user_test_data.get_invalid_emails()):
            with self.subTest(user_data=user_data):
                user_data['email'] = invalid_email
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserEmailException')
    
    def test_sign_up_invalid_name(self) -> None:
        for user_data, invalid_name in zip(DataFactory.generate_sign_up_request(),
                                           DataFactory.user_test_data.get_invalid_user_names()):
            with self.subTest(user_data=user_data):
                user_data['name'] = invalid_name
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserNameException')
    
    def test_sign_up_invalid_gender(self) -> None:
        for user_data in DataFactory.generate_sign_up_request():
            with self.subTest(user_data=user_data):
                user_data['gender'] = 'invalid'
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_birthdate(self) -> None:
        for user_data in DataFactory.generate_sign_up_request():
            with self.subTest(user_data=user_data):
                user_data['birthdate'] = DataFactory.user_test_data.get_invalid_birthdate().isoformat()
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserBirthdateException')
    
    def test_sign_up_invalid_password(self) -> None:
        for user_data, invalid_password in zip(DataFactory.generate_sign_up_request(),
                                               DataFactory.user_test_data.get_invalid_passwords()):
            with self.subTest(user_data=user_data):
                user_data['password'] = invalid_password
                response = self.client.post(self.route, user_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'InvalidUserPasswordException')

class UserAPITest(TestCase):
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
    
    def test_sign_in_incorrect_password(self) -> None:
        for user_data in self.user_request:
            with self.subTest(user_data=user_data):
                response = self.client.post(self.auth_route, {'phone_number': user_data['phone_number'], 'password': user_data['password']+'p'})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()['error'], 'IncorrectPasswordException')
    
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
                    self.assertEqual(response.json()['error'], 'ModelNotFoundException')