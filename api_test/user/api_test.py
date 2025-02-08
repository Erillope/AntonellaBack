from django.test import TestCase
from core.common import ID
from core.user import AccountStatus
from datetime import date
from .test_data import DataFactory

class AuthAPITest(TestCase):
    route = '/user'
    auth = '/user/auth'
    users_data = DataFactory.generate_sign_up_dtos()
    
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpClass()
        cls.client = cls.client_class()
        for role in DataFactory.user_test_data.get_roles():
            cls.client.post('/role', {'role': role})
    
    def test_sign_up(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                response = self.client.post(self.route, user_data.model_dump())
                data = response.json()['data']
                ID.validate(data['id'])
                self.assertEqual(data['status'], AccountStatus.ENABLE.name)
                self.assertEqual(data['created_date'], date.today().isoformat())
                self.assertEqual(data['email'], user_data.email.lower())
                self.assertEqual(data['name'], user_data.name.lower())
                self.assertEqual(data['roles'], [role.lower() for role in user_data.roles])
                self.assertEqual(data['phone_number'], user_data.phone_number)
                self.assertEqual(data['gender'], user_data.gender.name)
                self.assertEqual(data['birthdate'], user_data.birthdate.isoformat())
    
    def test_sign_up_email_already_exists(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                self.client.post(self.route, user_data.model_dump())
                user_data.phone_number = user_data.phone_number[0:5] + '0000'
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_phone_number_already_exists(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                self.client.post(self.route, user_data.model_dump())
                user_data.email = 'test_' + user_data.email
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_phone_number(self) -> None:
        for user_data, invalid_phone_number in zip(self.users_data,
                                                    DataFactory.user_test_data.get_invalid_phone_numbers()):
            with self.subTest(user_data=user_data):
                user_data.phone_number = invalid_phone_number
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_email(self) -> None:
        for user_data, invalid_email in zip(self.users_data,
                                            DataFactory.user_test_data.get_invalid_emails()):
            with self.subTest(user_data=user_data):
                user_data.email = invalid_email
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_name(self) -> None:
        for user_data, invalid_name in zip(self.users_data,
                                           DataFactory.user_test_data.get_invalid_user_names()):
            with self.subTest(user_data=user_data):
                user_data.name = invalid_name
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_gender(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                data = user_data.model_dump()
                data['gender'] = 'invalid'
                response = self.client.post(self.route, data)
                self.assertEqual(response.status_code, 400)
    
    def test_sing_up_invalid_birthdate(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                user_data.birthdate = DataFactory.user_test_data.get_invalid_birthdate()
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_up_invalid_password(self) -> None:
        for user_data, invalid_password in zip(self.users_data, DataFactory.user_test_data.get_invalid_passwords()):
            with self.subTest(user_data=user_data):
                user_data.password = invalid_password
                response = self.client.post(self.route, user_data.model_dump())
                self.assertEqual(response.status_code, 400)
    
    def test_sign_in(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                self.client.post(self.route, user_data.model_dump())
                response = self.client.post(self.auth, {'phone_number': user_data.phone_number, 'password': user_data.password})
                self.assertEqual(response.status_code, 200)
    
    def test_sign_in_incorrect_phone_number(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                response = self.client.post(self.auth, {'phone_number': user_data.phone_number+'0', 'password': user_data.password})
                self.assertEqual(response.status_code, 400)
    
    def test_sign_in_incorrect_password(self) -> None:
        for user_data in self.users_data:
            with self.subTest(user_data=user_data):
                response = self.client.post(self.auth, {'phone_number': user_data.phone_number, 'password': user_data.password+"p"})
                self.assertEqual(response.status_code, 400)