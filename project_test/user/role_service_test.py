import unittest
from core.user import RoleService, Role
from core.common import EventPublisher
from core.user.domain.events import RoleCreated, RoleUpdated
from project_test.mocks.repository_mocks import GetMock, SaveMock, DeleteMock
from .test_data import DataFactory

class RoleServiceTest(unittest.TestCase):
    get_role: GetMock[Role]
    save_role: SaveMock[Role]
    delete_role: DeleteMock[Role]
    role_service: RoleService
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.get_role = GetMock[Role]()
        cls.save_role = SaveMock[Role]((RoleCreated, RoleUpdated))
        cls.delete_role = DeleteMock[Role]()
        cls.role_service = RoleService(
            get_role=cls.get_role,
            delete_role=cls.delete_role
        )
        EventPublisher.subscribe(cls.save_role)
    
    @classmethod
    def tearDownClass(cls) -> None:
        EventPublisher.subscribers.clear()
        
    def test_create(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                role = self.role_service.create(rolename)
                self.assertEqual(role.name, rolename.lower())
                self.assertEqual(self.save_role.saved_model.name, role.name)
    
    def test_rename(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                role = self.role_service.rename(rolename, rolename)
                self.assertEqual(role.name, rolename.lower())
                self.assertEqual(self.save_role.saved_model.name, role.name)
    
    def test_get_all(self) -> None:
        self.get_role.get_all_return_value = DataFactory.generate_roles()
        roles = self.role_service.get_all()
        self.assertEqual(len(roles), len(self.get_role.get_all_return_value))
        for i in range(len(self.get_role.get_all_return_value)):
            self.assertEqual(roles[i].name, self.get_role.get_all_return_value[i].name)
    
    def test_delete(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                self.delete_role.delete_input_value = rolename
                self.role_service.delete(rolename)
                self.assertEqual(self.delete_role.deleted_model.name, rolename)