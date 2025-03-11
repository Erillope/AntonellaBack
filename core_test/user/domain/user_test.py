import unittest
from datetime import date
from core.user import UserAccountFactory, AccountStatus, UserAccount
from core.user.domain.values import UserPhoneNumber, UserEmail, UserName, UserPassword, Gender
from core.user.domain.exceptions import (InvalidPhoneNumberException, InvalidUserBirthdateException,
                                         InvalidUserEmailException, InvalidUserNameException, 
                                         InvalidUserPasswordException)
from ..test_data import UserDataFactory
import random
from typing import Dict, Any

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
    
    def _user_data(self) -> Dict[str, Any]:
        return {
            'phone_number': UserPhoneNumber.MATCHER.generate(),
            'email': UserEmail.MATCHER.generate(),
            'name': UserName.MATCHER.generate(),
            'password': UserPassword.MATCHER.generate(),
            'birthdate': UserDataFactory.get_birthdate(),
            'gender': random.choice(list(Gender))
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
    


'''class TestUserAccount(unittest.TestCase):        
    def test_update_user_account(self) -> None:
        for phone_number, email, name, password, user in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords(),
            DataFactory.generate_user_accounts()
        ):
            status = DataFactory.user_test_data.get_account_status()
            with self.subTest(phone_number=phone_number, email=email, name=name, password=password, status=status):
                user.change_data(phone_number=phone_number, email=email, name=name, password=password, status=status)
                self.assertEqual(user.phone_number, phone_number)
                self.assertEqual(user.email, email.lower())
                self.assertEqual(user.name, name.lower())
                self.assertTrue(user.verify_password(password))
                self.assertEqual(user.status, status)
    
    def test_false_update_user_account(self) -> None:
        for user in DataFactory.generate_user_accounts():
            with self.subTest(user=user):
                user.change_data()
    
    def test_verify_password(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.assertTrue(user.verify_password(password))
    
    def test_verify_account(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.assertTrue(user.verify_account(phone_number, password))
                self.assertFalse(user.verify_account(phone_number, password+'1'))
                other_phone_number = phone_number[:3] + str((int(phone_number[3])+1)%10) + phone_number[4:]
                self.assertFalse(user.verify_account(other_phone_number, password))
    
    def test_add_role(self) -> None:
        for user, role in zip(DataFactory.generate_user_accounts(), DataFactory.generate_sample_roles()):
            with self.subTest(user=user, role=role):
                user.add_role(role)
                self.assertTrue(role in user.roles)
    
    def test_remove_role(self) -> None:
        for user, role in zip(DataFactory.generate_user_accounts(), DataFactory.generate_sample_roles()):
            with self.subTest(user=user, role=role):
                user.add_role(role)
                self.assertTrue(role in user.roles)
                user.remove_role(role)
                self.assertFalse(role in user.roles)'''