import unittest
from core.user import RoleService, Role
from core.user.service.exceptions import AlreadyExistsRoleException
from core_test.mocks.repository_mocks import GetMock
from ..test_data import DataFactory

class RoleServiceTest(unittest.TestCase):
    get_role: GetMock[Role]
    role_service: RoleService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_role = GetMock[Role]()
        cls.role_service = RoleService(
            get_role=cls.get_role,
        )
        
    def test_create(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.get_role.exists_input_return_values = [(rolename, False)]
                role = self.role_service.create(rolename)
                self.assertEqual(role.name, rolename.lower())
    
    def test_rename(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                self.get_role.exists_input_return_values = [(role.name, False)]
                self.get_role.get_input_return_values = [(role.name, role)]
                role_dto = self.role_service.rename(role.name, "renamed")
                self.assertEqual(role_dto.name, role.name)

    def test_create_already_exists(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.get_role.exists_input_return_values = [(rolename, True)]
                with self.assertRaises(AlreadyExistsRoleException):
                    self.role_service.create(rolename)
    
    def rename_already_exists(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.get_role.exists_input_return_values = [(rolename, True)]
                with self.assertRaises(AlreadyExistsRoleException):
                    self.role_service.rename(rolename, rolename)
                    
    def test_get_all(self) -> None:
        self.get_role.get_all_return_value = DataFactory.generate_roles()
        roles = self.role_service.get_all()
        self.assertEqual(len(roles), len(self.get_role.get_all_return_value))
        for i in range(len(self.get_role.get_all_return_value)):
            self.assertEqual(roles[i].name, self.get_role.get_all_return_value[i].name)
    
    def test_delete(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                self.get_role.get_input_return_values = [(role.name, role)]
                self.role_service.delete(role.name)