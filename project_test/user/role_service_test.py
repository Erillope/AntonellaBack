import unittest
from core.user import RoleService, Role, RoleFactory
from core.common import ID
from core.user.domain.events import RoleCreated, RoleUpdated
from project_test.mocks.repository_mocks import GetMock, SaveMock, DeleteMock
from datetime import date

class RoleServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.get_role = GetMock[Role]()
        self.save_role = SaveMock[Role]((RoleCreated, RoleUpdated))
        self.delete_role = DeleteMock[Role]()
        self.role_service = RoleService(
            get_role=self.get_role,
            delete_role=self.delete_role
        )
        
        self.sample_rolename = 'admin'
        
        self.sample_role = RoleFactory.load(
            ID.generate(),
            self.sample_rolename,
            date.today()
        )
        
    def test_create(self) -> None:
        self.get_role.get_input_value = self.sample_rolename
        self.get_role.get_return_value = RoleFactory.load(
            ID.generate(),
            self.sample_rolename,
            date.today()
        )
        role = self.role_service.create(self.sample_rolename)
        self.assertEqual(role.name, self.sample_rolename)
        self.assertEqual(self.save_role.saved_model.name, role.name)
    
    def test_rename(self) -> None:
        role = self.role_service.rename(self.sample_rolename, self.sample_rolename)
        self.assertEqual(role.name, self.sample_rolename)
        self.assertEqual(self.save_role.saved_model.name, role.name)
    
    def test_get_all(self) -> None:
        self.get_role.get_all_return_value = [
            RoleFactory.load(ID.generate(), 'admin', date.today()),
            RoleFactory.load(ID.generate(), 'user', date.today())
        ]
        roles = self.role_service.get_all()
        self.assertEqual(len(roles), 2)
        for i in range(len(self.get_role.get_all_return_value)):
            self.assertEqual(roles[i].name, self.get_role.get_all_return_value[i].name)
    
    def test_delete(self) -> None:
        self.delete_role.delete_input_value = self.sample_rolename
        self.role_service.delete(self.sample_rolename)
        self.assertEqual(self.delete_role.deleted_model.name, self.sample_rolename)