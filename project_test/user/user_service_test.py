import unittest
from core.user import AuthService, UserAccount, UpdateUserService
from core.common import EventPublisher, ID
from core.user.domain.events import UserAccountCreated, UserAccountUpdated
from core.user.service.exceptions import IncorrectPasswordException
from project_test.mocks.repository_mocks import GetMock, SaveMock
from .test_data import DataFactory

class AuthServiceTest(unittest.TestCase):
    get_user: GetMock[UserAccount]
    save_user: SaveMock[UserAccount]
    auth_service: AuthService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_user = GetMock[UserAccount]()
        cls.save_user = SaveMock[UserAccount]((UserAccountCreated, UserAccountUpdated))
        cls.auth_service = AuthService(
            get_user=cls.get_user
        )
        EventPublisher.subscribe(cls.save_user)
    
    @classmethod
    def tearDownClass(cls) -> None:
        EventPublisher.subscribers.clear()
    
    def test_sign_up(self) -> None:
        for sign_up_dto in DataFactory.generate_sign_up_dtos():
            with self.subTest(sign_up_dto=sign_up_dto):
                user = self.auth_service.sign_up(sign_up_dto)
                self.assertEqual(self.save_user.saved_model.id, user.id)
        
    def test_sign_in(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.get_user.get_input_value = phone_number
                self.get_user.get_return_value = user
                self.auth_service.sign_in(phone_number, password)
    
    def test_failed_sign_in(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.get_user.get_input_value = phone_number
                self.get_user.get_return_value = user
                with self.assertRaises(IncorrectPasswordException):
                    self.auth_service.sign_in(phone_number, password + '1')