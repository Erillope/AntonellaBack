import unittest
from core.user import RoleFactory
from core.user.domain.exceptions import InvalidRoleException
from core.common import ID
from core.common.exceptions import InvalidIdException
from datetime import date
from .test_data import DataFactory

class TestRoleCreation(unittest.TestCase):    
    def test_create_role(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                role = RoleFactory.create(name=rolename)
                self.assertEqual(role.name, rolename.lower())
                self.assertTrue(role.created_date == date.today())
        
    def test_load_role(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            created_date = DataFactory.user_test_data.get_created_date()
            id = ID.generate()
            with self.subTest(id=id, rolename=rolename, created_date=created_date):
                role = RoleFactory.load(id=id, name=rolename, created_date=created_date)
                self.assertEqual(role.id, id)
                self.assertEqual(role.name, rolename.lower())
                self.assertEqual(role.created_date, created_date)
        
    def test_invalid_role_name(self) -> None:
        for invalid_rolename in DataFactory.user_test_data.get_invalid_roles():
            with self.subTest(invalid_rolename=invalid_rolename):
                with self.assertRaises(InvalidRoleException):
                    RoleFactory.create(name=invalid_rolename)

    def test_invalid_role_id(self) -> None:
        for invalid_id in DataFactory.user_test_data.get_invalid_ids():
            with self.subTest(invalid_id=invalid_id):
                with self.assertRaises(InvalidIdException):
                    RoleFactory.load(id=invalid_id, name="admin", created_date=date.today())
                    

class TestRole(unittest.TestCase):
    def test_rename_role(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                role = RoleFactory.create(name=rolename)
                role.rename(name=rolename)
                self.assertEqual(role.name, rolename.lower())

    
    def test_invalid_role_name(self) -> None:
        for invalid_rolename, role in zip(DataFactory.user_test_data.get_invalid_roles(), DataFactory.generate_roles()):
            with self.subTest(role=role, invalid_rolename=invalid_rolename):
                with self.assertRaises(InvalidRoleException):
                    role.rename(name=invalid_rolename)