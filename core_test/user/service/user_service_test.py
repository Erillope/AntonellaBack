import unittest
from core.user import AuthService, UserAccount, UpdateUserService
from core.user.service.exceptions import IncorrectPasswordException
from core_test.mocks.repository_mocks import GetMock
from ..test_data import DataFactory

class AuthServiceTest(unittest.TestCase):
    get_user: GetMock[UserAccount]
    auth_service: AuthService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_user = GetMock[UserAccount]()
        cls.auth_service = AuthService(
            get_user=cls.get_user
        )
    
    def test_sign_up(self) -> None:
        for sign_up_dto in DataFactory.generate_sign_up_dtos():
            with self.subTest(sign_up_dto=sign_up_dto):
                self.get_user.exists_input_return_values = [(sign_up_dto.phone_number, False), (sign_up_dto.email, False)]
                user = self.auth_service.sign_up(sign_up_dto)
        
    def test_sign_in(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.get_user.get_input_return_values = [(phone_number, user)]
                self.auth_service.sign_in(phone_number, password)
    
    def test_failed_sign_in(self) -> None:
        for user, phone_number, password in DataFactory.generate_user_with_info():
            with self.subTest(user=user, phone_number=phone_number, password=password):
                self.get_user.get_input_return_values = [(phone_number, user)]
                with self.assertRaises(IncorrectPasswordException):
                    self.auth_service.sign_in(phone_number, password + '1')


class UpdateUserServiceTest(unittest.TestCase):
    get_user: GetMock[UserAccount]
    update_user_service: UpdateUserService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_user = GetMock[UserAccount]()
        cls.update_user_service = UpdateUserService(
            get_user=cls.get_user
        )
    
    def test_update_user(self) -> None:
        for user, update_user_dto in DataFactory.generate_user_and_update_dto():
            with self.subTest(user=user, update_user_dto=update_user_dto):
                self.get_user.exists_input_return_values = []
                if update_user_dto.phone_number:
                    self.get_user.exists_input_return_values = [(update_user_dto.phone_number, False)]
                if update_user_dto.email:
                    self.get_user.exists_input_return_values += [(update_user_dto.email, False)]
                self.get_user.get_input_return_values = [(user.id, user)]
                self.update_user_service.update_user(update_user_dto)
    
    def test_add_role(self) -> None:
        for user, role in zip(DataFactory.generate_user_accounts(), DataFactory.user_test_data.get_roles()):
            with self.subTest(user=user, role=role):
                self.get_user.get_input_return_values = [(user.id, user)]
                self.update_user_service.add_role(user.id, role)
    
    def test_remove_role(self) -> None:
        for user in DataFactory.generate_user_accounts():
            with self.subTest(user=user):
                self.get_user.get_input_return_values = [(user.id, user)]
                self.update_user_service.remove_role(user.id, user.roles[0].name)