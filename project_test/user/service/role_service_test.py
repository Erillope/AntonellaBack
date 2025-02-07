import unittest
from core.user import RoleService, Role
from core.user.service.exceptions import AlreadyExistsRoleException
from project_test.mocks.repository_mocks import GetMock, DeleteMock
from ..test_data import DataFactory

class RoleServiceTest(unittest.TestCase):
    get_role: GetMock[Role]
    delete_role: DeleteMock[Role]
    role_service: RoleService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_role = GetMock[Role]()
        cls.delete_role = DeleteMock[Role]()
        cls.role_service = RoleService(
            get_role=cls.get_role,
            delete_role=cls.delete_role
        )
        
    def test_create(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.get_role.exists_input_return_values = [(rolename, False)]
                role = self.role_service.create(rolename)
                self.assertEqual(role.name, rolename.lower())
    
    def test_rename(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.get_role.exists_input_return_values = [(rolename, False)]
                role = self.role_service.rename(rolename, rolename)
                self.assertEqual(role.name, rolename.lower())

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
                self.delete_role.delete_input_return_values = (role.name, role)
                self.role_service.delete(role.name)