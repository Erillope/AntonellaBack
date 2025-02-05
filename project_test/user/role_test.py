import unittest
from core.user import RoleFactory
from core.user.domain.events import RoleCreated, RoleUpdated
from core.user.domain.exceptions import InvalidRoleException
from core.common import ID, EventPublisher
from datetime import date

class TestRoleCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_rolename = 'admin'
        self.sample_id = ID.generate()
        self.sample_created_date = date.today()
        self.invalid_rolename = "si"
        self.invalid_id = "12345"
    
    def test_create_role(self) -> None:
        EventPublisher.clear()
        role = RoleFactory.create(name=self.sample_rolename)
        self.assertEqual(role.name, self.sample_rolename)
        self.assertTrue(role.created_date == date.today())
        self.assertTrue(len(EventPublisher.get_events()) == 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, RoleCreated), )
        
    def test_load_role(self) -> None:
        role = RoleFactory.load(id=self.sample_id, name=self.sample_rolename,
                                created_date=self.sample_created_date)
        self.assertEqual(role.id, self.sample_id)
        self.assertEqual(role.name, self.sample_rolename)
        self.assertEqual(role.created_date, self.sample_created_date)
        self.assertEqual(len(EventPublisher.get_events()), 0)
        
    def test_invalid_role_name(self) -> None:
        with self.assertRaises(InvalidRoleException):
            RoleFactory.create(name=self.invalid_rolename)
    
    def test_invalid_role_id(self) -> None:
        with self.assertRaises(InvalidRoleException):
            RoleFactory.load(id=self.invalid_id, name=self.sample_rolename,
                             created_date=self.sample_created_date)


class TestRole(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_role = RoleFactory.create(name='admin')
        self.sample_rolename = "admin2"
        self.invalid_rolename = "si"
    
    def test_rename_role(self) -> None:
        EventPublisher.clear()
        self.sample_role.rename(name=self.sample_rolename)
        self.assertEqual(self.sample_role.name, self.sample_rolename)
        self.assertEqual(len(EventPublisher.get_events()), 1)
        event = EventPublisher.get_events()[0]
        self.assertTrue(isinstance(event, RoleUpdated))
    
    def test_invalid_role_name(self) -> None:
        with self.assertRaises(InvalidRoleException):
            self.sample_role.rename(name=self.invalid_rolename)