import unittest
from core.common import ID
from datetime import date
from core.user import UserAccountFactory, AccountStatus
from core.user.domain.exceptions import (InvalidPhoneNumberException, InvalidUserBirthdateException,
                                         InvalidUserEmailException, InvalidUserNameException, 
                                         InvalidUserPasswordException)
from .test_data import DataFactory

class TestUserAccountCreation(unittest.TestCase):
    def test_user_account_creation(self) -> None:
        for phone_number, email, name, password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(phone_number=phone_number, email=email, name=name, password=password,
                              birthdate=birthdate, roles=roles, gender=gender):
                user = UserAccountFactory.create(
                    phone_number=phone_number,
                    email=email,
                    name=name,
                    password=password,
                    birthdate=birthdate,
                    roles=roles,
                    gender=gender
                )
                self.assertEqual(user.phone_number, phone_number)
                self.assertEqual(user.email, email)
                self.assertEqual(user.name, name)
                self.assertTrue(user.verify_password(password))
                self.assertEqual(user.birthdate, birthdate)
                self.assertEqual(user.roles, roles)
                self.assertTrue(user.status == AccountStatus.ENABLE)
                self.assertTrue(user.created_date == date.today())
                self.assertEqual(user.gender, gender)

    def test_user_account_load(self) -> None:
        for phone_number, email, name, password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            id = ID.generate()
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            created_date = DataFactory.user_test_data.get_created_date()
            gender = DataFactory.user_test_data.get_gender()
            status = DataFactory.user_test_data.get_account_status()
            with self.subTest(id=id, phone_number=phone_number, email=email, name=name, password=password,
                                birthdate=birthdate, roles=roles, created_date=created_date, gender=gender,
                                status=status):
                
                user = UserAccountFactory.load(
                    id=id,
                    phone_number=phone_number,
                    email=email,
                    name=name,
                    password=password,
                    status=status,
                    birthdate=birthdate,
                    created_date=created_date,
                    roles=roles,
                    gender=gender
                )        
                self.assertEqual(user.id, id)
                self.assertEqual(user.status, status)
                self.assertEqual(user.created_date, created_date)
    
    def test_invalid_phone_number(self) -> None:
        for invalid_phone_number, email, name, password in zip(
            DataFactory.user_test_data.get_invalid_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(invalid_phone_number=invalid_phone_number, email=email, name=name,
                            password=password, birthdate=birthdate, roles=roles, gender=gender):
                with self.assertRaises(InvalidPhoneNumberException):
                    UserAccountFactory.create(phone_number=invalid_phone_number, email=email,
                                            name=name, password=password,
                                            birthdate=birthdate, roles=roles,
                                            gender=gender)
            
    def test_invalid_email(self) -> None:
        for phone_number, invalid_email, name, password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_invalid_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(phone_number=phone_number, invalid_email=invalid_email, name=name,
                              password=password, birthdate=birthdate, roles=roles, gender=gender):
                with self.assertRaises(InvalidUserEmailException):
                    UserAccountFactory.create(phone_number=phone_number, email=invalid_email,
                                              name=name, password=password,
                                              birthdate=birthdate, roles=roles,
                                              gender=gender)
    
    def test_invalid_name(self) -> None:
        for phone_number, email, invalid_name, password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_invalid_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(phone_number=phone_number, email=email, invalid_name=invalid_name,
                              password=password, birthdate=birthdate, roles=roles, gender=gender):
                with self.assertRaises(InvalidUserNameException):
                    UserAccountFactory.create(phone_number=phone_number, email=email,
                                              name=invalid_name, password=password,
                                              birthdate=birthdate, roles=roles,
                                              gender=gender)
    
    def test_invalid_password(self) -> None:
        for phone_number, email, name, invalid_password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_invalid_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(phone_number=phone_number, email=email, name=name,
                              invalid_password=invalid_password, birthdate=birthdate, roles=roles, gender=gender):
                with self.assertRaises(InvalidUserPasswordException):
                    UserAccountFactory.create(phone_number=phone_number, email=email,
                                              name=name, password=invalid_password,
                                              birthdate=birthdate, roles=roles,
                                              gender=gender)
    
    def test_invalid_birthdate(self) -> None:
        for phone_number, email, name, password in zip(
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords(),
        ):
            invalid_birthdate = DataFactory.user_test_data.get_invalid_birthdate()
            roles = DataFactory.generate_sample_roles()
            gender = DataFactory.user_test_data.get_gender()
            with self.subTest(phone_number=phone_number, email=email, name=name,
                              password=password, invalid_birthdate=invalid_birthdate, roles=roles, gender=gender):
                with self.assertRaises(InvalidUserBirthdateException):
                    UserAccountFactory.create(phone_number=phone_number, email=email,
                                              name=name, password=password,
                                              birthdate=invalid_birthdate, roles=roles,
                                              gender=gender)
    
    def test_invalid_id(self) -> None:
        for invalid_id, phone_number, email, name, password in zip(
            DataFactory.user_test_data.get_invalid_ids(),
            DataFactory.user_test_data.get_phone_numbers(),
            DataFactory.user_test_data.get_emails(),
            DataFactory.user_test_data.get_user_names(),
            DataFactory.user_test_data.get_passwords()
        ):
            birthdate = DataFactory.user_test_data.get_birthdate()
            roles = DataFactory.generate_sample_roles()
            created_date = DataFactory.user_test_data.get_created_date()
            gender = DataFactory.user_test_data.get_gender()
            status = DataFactory.user_test_data.get_account_status()
            with self.subTest(invalid_id=invalid_id, phone_number=phone_number, email=email, name=name,
                              password=password, birthdate=birthdate, roles=roles, created_date=created_date,
                              gender=gender, status=status):
                with self.assertRaises(InvalidUserBirthdateException):
                    UserAccountFactory.load(id=invalid_id, phone_number=phone_number,
                                            email=email, name=name,
                                            password=password, status=status,
                                            birthdate=birthdate, created_date=created_date,
                                            roles=roles, gender=gender)


class TestUserAccount(unittest.TestCase):        
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
                self.assertEqual(user.email, email)
                self.assertEqual(user.name, name)
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
                other_phone_number = phone_number[:3] + '1' + phone_number[4:]
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
                self.assertFalse(role in user.roles)