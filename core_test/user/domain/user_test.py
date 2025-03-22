import unittest
from datetime import date
from core.user import UserAccountFactory, AccountStatus, UserAccount, Role, EmployeeAccount
from core.user.domain.values import UserPhoneNumber, UserEmail, UserName, UserPassword, Gender, DniValue, EmployeeCategories
from core.user.domain.exceptions import (InvalidPhoneNumberException, InvalidUserBirthdateException,
                                         InvalidUserEmailException, InvalidUserNameException, 
                                         InvalidUserPasswordException)
from ..test_data import UserDataFactory
import random
import string
from typing import Dict, Any, List
from core_test.images_data import get_base64_string

class TestUserAccountCreation(unittest.TestCase):
    num_test = 10
    
    def test_user_account_creation(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            with self.subTest(**user_data):
                user = UserAccountFactory.create_user(**user_data)
                self._validate_user(user, **user_data)
    
        
    def test_invalid_phone_number(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            user_data['phone_number'] = UserPhoneNumber.MATCHER.generate_invalid(random.randint(0,10))
            with self.subTest(**user_data):
                with self.assertRaises(InvalidPhoneNumberException):
                    UserAccountFactory.create_user(**user_data)
            
    def test_invalid_email(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            user_data['email'] = UserEmail.MATCHER.generate_invalid(random.randint(0,20))
            with self.subTest(**user_data):
                with self.assertRaises(InvalidUserEmailException):
                    UserAccountFactory.create_user(**user_data)
    
    def test_invalid_name(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            user_data['name'] = 'invalid name'
            with self.subTest(**user_data):
                with self.assertRaises(InvalidUserNameException):
                    UserAccountFactory.create_user(**user_data)
    
    def test_invalid_password(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            user_data['password'] = UserPassword.MATCHER.generate_invalid(random.randint(0,20))
            with self.subTest(**user_data):
                with self.assertRaises(InvalidUserPasswordException):
                    UserAccountFactory.create_user(**user_data)
    
    def test_invalid_birthdate(self) -> None:
        for _ in range(self.num_test):
            user_data = self._user_data()
            user_data['birthdate'] = UserDataFactory.get_invalid_birthdate()
            with self.subTest(**user_data):
                with self.assertRaises(InvalidUserBirthdateException):
                    UserAccountFactory.create_user(**user_data)
    
    def test_update_user_account(self) -> None:
        for _ in range(self.num_test):
            user = UserDataFactory.generate_user_account()
            user_data = self._user_data()
            user_data.pop('password')
            with self.subTest(user=user, **user_data):
                user.change_data(**user_data)
                user.change_data(status=AccountStatus.DISABLE)
    
    
    def test_create_employee_account(self) -> None:
        for _ in range(self.num_test):
            employee_data = self._employee_data()
            with self.subTest():
                employee = UserAccountFactory.create_employee(**employee_data)
                employee_data.pop('photo')
                self._validate_employee(employee, **employee_data)
                
    def _user_data(self) -> Dict[str, Any]:
        return {
            'phone_number': UserPhoneNumber.MATCHER.generate(),
            'email': UserEmail.MATCHER.generate(),
            'name': UserName.MATCHER.generate(),
            'password': UserPassword.MATCHER.generate(),
            'birthdate': UserDataFactory.get_birthdate(),
            'gender': random.choice(list(Gender))
        }
    
    def _employee_data(self) -> Dict[str, Any]:
        return {
            'phone_number': UserPhoneNumber.MATCHER.generate(),
            'email': UserEmail.MATCHER.generate(),
            'name': UserName.MATCHER.generate(),
            'password': UserPassword.MATCHER.generate(),
            'birthdate': UserDataFactory.get_birthdate(),
            'gender': random.choice(list(Gender)),
            'dni': DniValue.MATCHER.generate(),
            'address': ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
            'roles': [Role.MATCHER.generate() for _ in range(random.randint(1,5))],
            'photo': get_base64_string(),
            'categories': random.sample(list(EmployeeCategories), random.randint(1,3))
        }
        
    def _validate_user(self, user: UserAccount, phone_number: str, email: str, name: str, password: str, gender: Gender, birthdate: date) -> None:
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.email, email.lower())
        self.assertEqual(user.name, name.lower())
        self.assertTrue(user.verify_password(password))
        self.assertEqual(user.birthdate, birthdate)
        self.assertTrue(user.status == AccountStatus.ENABLE)
        self.assertTrue(user.created_date == date.today())
        self.assertEqual(user.gender, gender)
    
    def _validate_employee(self, user: EmployeeAccount, phone_number: str, email: str, name: str, password: str, gender: Gender, birthdate: date, dni: str, address: str, roles: List[str], categories: List[EmployeeCategories]) -> None:
        self._validate_user(user, phone_number, email, name, password, gender, birthdate)
        self.assertEqual(user.dni, dni)
        self.assertEqual(user.address, address)
        self.assertIsNotNone(user.photo)
        self.assertEqual(user.roles, roles)
        self.assertEqual(user.categories, categories)