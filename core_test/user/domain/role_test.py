import unittest
from core.user import RoleFactory, Role
from core.user.domain.values import RoleAccess
from core.user.domain.exceptions import InvalidRoleException
from datetime import date
import random
from ..test_data import UserDataFactory
from typing import Set

class TestRole(unittest.TestCase):    
    num_test = 10
    
    def test_create_role(self) -> None:
        for _ in range(self.num_test):
            name = Role.MATCHER.generate()
            accesses = {UserDataFactory.generate_role_access() for _ in range(random.randint(1, 5))}
            with self.subTest(name=name, accesses=accesses):
                role = RoleFactory.create(
                    name=name,
                    accesses=accesses
                )
                self._validate_role(role, name, accesses)
    
    def test_invalid_role_name(self) -> None:
        for _ in range(self.num_test):
            invalid_name = Role.MATCHER.generate_invalid(50)
            accesses = {UserDataFactory.generate_role_access() for _ in range(random.randint(1, 5))}
            with self.subTest(invalid_name=invalid_name, accesses=accesses):
                with self.assertRaises(InvalidRoleException):
                    RoleFactory.create(
                        name=invalid_name,
                        accesses=accesses
                    )
    
    def test_rename_role(self) -> None:
        for _ in range(self.num_test):
            role = UserDataFactory.generate_role()
            new_name = Role.MATCHER.generate()
            with self.subTest(role=role, new_name=new_name):
                role.rename(new_name)
                self.assertEqual(role.name, new_name.lower())
    
    def test_invalid_rename_role(self) -> None:
        for _ in range(self.num_test):
            role = UserDataFactory.generate_role()
            invalid_name = Role.MATCHER.generate_invalid(50)
            with self.subTest(role=role, invalid_name=invalid_name):
                with self.assertRaises(InvalidRoleException):
                    role.rename(invalid_name)
                
    def _validate_role(self, role: Role, name: str, accesses: Set[RoleAccess]) -> None:
        self.assertEqual(role.name, name.lower())
        self.assertEqual(role.accesses, accesses)
        self.assertEqual(role.created_date, date.today())
            
            
    '''             
class TestRole(unittest.TestCase):
    
    def test_invalid_role_name(self) -> None:
        for invalid_rolename, role in zip(DataFactory.user_test_data.get_invalid_roles(), DataFactory.generate_roles()):
            with self.subTest(role=role, invalid_rolename=invalid_rolename):
                with self.assertRaises(InvalidRoleException):
                    role.rename(name=invalid_rolename)'''