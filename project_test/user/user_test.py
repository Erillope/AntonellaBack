import unittest
from core.common import ID, EventPublisher
from datetime import date
from core.user import UserAccountFactory, AccountStatus, RoleFactory
from core.user.domain.events import (UserAccountCreated, UserAccountUpdated, RoleAddedToUser, 
                                     RoleRemovedFromUser)
from core.user.domain.exceptions import (InvalidPhoneNumberException, InvalidUserBirthdateException,
                                         InvalidUserEmailException, InvalidUserNameException, 
                                         InvalidUserPasswordException)
from copy import deepcopy

class TestUserAccountCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_id = ID.generate()
        self.sample_phone_number = "0981530739"
        self.sample_email = "erillope@gmail.com"
        self.sample_name = "Erick"
        self.sample_password = "Contraseña-123"
        self.sample_birthdate = date(1998, 10, 10)
        self.sample_roles = [RoleFactory.create(name="admin"), RoleFactory.create(name="employee")]
        self.sample_status = AccountStatus.DISABLE
        self.sample_created_date = date(2021, 10, 10)
        self.invalid_id = "12345"
        self.invalid_phone_number = "123456789"
        self.invalid_email = "erickgmail.com"
        self.invalid_name = "er"
        self.invalid_password = "contraseña"
        self.invalid_birthdate = date.today()
    
    def test_user_account_creation(self) -> None:
        EventPublisher.clear()
        user = UserAccountFactory.create(phone_number=self.sample_phone_number, email=self.sample_email,
                                         name=self.sample_name, password=self.sample_password,
                                         birthdate=self.sample_birthdate, roles=self.sample_roles)
        self.assertEqual(user.phone_number, self.sample_phone_number)
        self.assertEqual(user.email, self.sample_email)
        self.assertEqual(user.name, self.sample_name)
        self.assertTrue(user.verify_password(self.sample_password))
        self.assertEqual(user.birthdate, self.sample_birthdate)
        self.assertEqual(user.roles, self.sample_roles)
        self.assertTrue(user.status == AccountStatus.ENABLE)
        self.assertTrue(user.created_date == date.today())
        self.assertTrue(len(EventPublisher.get_events()) == 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, UserAccountCreated))
    
    def test_user_account_load(self) -> None:
        user = UserAccountFactory.load(id=self.sample_id, phone_number=self.sample_phone_number,
                                       email=self.sample_email, name=self.sample_name,
                                       password=self.sample_password, status=self.sample_status,
                                       birthdate=self.sample_birthdate, created_date=date.today(),
                                       roles=self.sample_roles)
        self.assertEqual(user.id, self.sample_id)
        self.assertEqual(user.roles, self.sample_roles)
        self.assertEqual(user.status, self.sample_status)
        self.assertEqual(user.created_date, self.sample_created_date)
        self.assertEqual(user.phone_number, self.sample_phone_number)
        self.assertTrue(len(EventPublisher.get_events()) == 0)
    
    def test_invalid_phone_number(self) -> None:
        with self.assertRaises(InvalidPhoneNumberException):
            UserAccountFactory.create(phone_number=self.invalid_phone_number, email=self.sample_email,
                                      name=self.sample_name, password=self.sample_password,
                                      birthdate=self.sample_birthdate, roles=self.sample_roles)
            
    def test_invalid_email(self) -> None:
        with self.assertRaises(InvalidUserEmailException):
            UserAccountFactory.create(phone_number=self.sample_phone_number, email=self.invalid_email,
                                      name=self.sample_name, password=self.sample_password,
                                      birthdate=self.sample_birthdate, roles=self.sample_roles)
    
    def test_invalid_name(self) -> None:
        with self.assertRaises(InvalidUserNameException):
            UserAccountFactory.create(phone_number=self.sample_phone_number, email=self.sample_email,
                                      name=self.invalid_name, password=self.sample_password,
                                      birthdate=self.sample_birthdate, roles=self.sample_roles)
    
    def test_invalid_password(self) -> None:
        with self.assertRaises(InvalidUserPasswordException):
            UserAccountFactory.create(phone_number=self.sample_phone_number, email=self.sample_email,
                                      name=self.sample_name, password=self.invalid_password,
                                      birthdate=self.sample_birthdate, roles=self.sample_roles)
    
    def test_invalid_birthdate(self) -> None:
        with self.assertRaises(InvalidUserBirthdateException):
            UserAccountFactory.create(phone_number=self.sample_phone_number, email=self.sample_email,
                                      name=self.sample_name, password=self.sample_password,
                                      birthdate=self.invalid_birthdate, roles=self.sample_roles)
    
    def test_invalid_id(self) -> None:
        with self.assertRaises(InvalidUserBirthdateException):
            UserAccountFactory.load(id=self.invalid_id, phone_number=self.sample_phone_number,
                                    email=self.sample_email, name=self.sample_name,
                                    password=self.sample_password, status=self.sample_status,
                                    birthdate=self.sample_birthdate, created_date=date.today(),
                                    roles=self.sample_roles)


class TestUserAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_user_password = "Contraseña-123"
        self.sample_user_phone_number = "0981530739"
        self.sample_user = UserAccountFactory.create(
            phone_number=self.sample_user_phone_number,
            email="erick@gmail.com",
            name="Erick",
            password=self.sample_user_password,
            birthdate=date(2004, 9, 28),
            roles=[RoleFactory.create(name="admin"), RoleFactory.create(name="employee")]
        )
        self.sample_user2 = deepcopy(self.sample_user)
        self.sample_name = "Erick2"
        self.sample_phone_number = "0981043216"
        self.sample_email = "erick2@gmail.com"
        self.sample_password = "ContraseñaNueva-1234"
        self.sample_status = AccountStatus.DISABLE
        self.invalid_phone_number = "123456789"
        self.invalid_email = "erickgmail.com"
        self.invalid_name = "er"
        self.invalid_password = "contraseña"
        self.sample_role = RoleFactory.create(name="nuevo")
        
    def test_update_user_account(self) -> None:
        EventPublisher.clear()
        self.sample_user.change_data(
            phone_number=self.sample_phone_number,
            email=self.sample_email,
            name=self.sample_name,
            password=self.sample_password,
            status=self.sample_status
        )
        self.assertEqual(self.sample_user.phone_number, self.sample_phone_number)
        self.assertEqual(self.sample_user.email, self.sample_email)
        self.assertEqual(self.sample_user.name, self.sample_name)
        self.assertTrue(self.sample_user.verify_password(self.sample_password))
        self.assertEqual(self.sample_user.status, self.sample_status)
        self.assertEqual(len(EventPublisher.get_events()), 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, UserAccountUpdated))
    
    def test_invalid_phone_number(self) -> None:
        with self.assertRaises(InvalidPhoneNumberException):
            self.sample_user.change_data(
                phone_number=self.invalid_phone_number,
                email=self.sample_email,
                name=self.sample_name,
                password=self.sample_password,
                status=self.sample_status
            )
    
    def test_invalid_email(self) -> None:
        with self.assertRaises(InvalidUserEmailException):
            self.sample_user.change_data(
                phone_number=self.sample_phone_number,
                email=self.invalid_email,
                name=self.sample_name,
                password=self.sample_password,
                status=self.sample_status
            )
    
    def test_invalid_name(self) -> None:
        with self.assertRaises(InvalidUserNameException):
            self.sample_user.change_data(
                phone_number=self.sample_phone_number,
                email=self.sample_email,
                name=self.invalid_name,
                password=self.sample_password,
                status=self.sample_status
            )
    
    def test_invalid_password(self) -> None:
        with self.assertRaises(InvalidUserPasswordException):
            self.sample_user.change_data(
                phone_number=self.sample_phone_number,
                email=self.sample_email,
                name=self.sample_name,
                password=self.invalid_password,
                status=self.sample_status
            )
    
    def test_verify_password(self) -> None:
        self.assertTrue(self.sample_user2.verify_password(self.sample_user_password))
        self.assertFalse(self.sample_user2.verify_password(self.sample_password))
    
    def test_verify_account(self) -> None:
        self.assertTrue(self.sample_user2.verify_account(self.sample_user_phone_number, self.sample_user_password))
        self.assertFalse(self.sample_user2.verify_account(self.sample_phone_number, self.sample_password))
        self.assertFalse(self.sample_user2.verify_account(self.sample_phone_number, self.sample_user_password))
    
    def test_add_role(self) -> None:
        EventPublisher.clear()
        self.sample_user.add_role(self.sample_role)
        self.assertTrue(self.sample_role in self.sample_user.roles)
        self.assertEqual(len(EventPublisher.get_events()), 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, RoleAddedToUser))
    
    def test_remove_role(self) -> None:
        EventPublisher.clear()
        removed_role = self.sample_user.roles[0]
        self.sample_user.remove_role(removed_role)
        self.assertTrue(removed_role not in self.sample_user.roles)
        self.assertEqual(len(EventPublisher.get_events()), 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, RoleRemovedFromUser))