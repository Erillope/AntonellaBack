from django.test import TestCase
from app.user.mapper import UserTableMapper, RoleTableMapper
from app.user.models import UserRoleTableData
from .test_data import DataFactory

class TestUserTableMapper(TestCase):
    user_mapper: UserTableMapper
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_mapper = UserTableMapper()
        cls.role_mapper = RoleTableMapper()
    
    def test_to_user(self) -> None:
        for user_table in DataFactory.generate_user_tables():
            user_table.save()
            with self.subTest(user_table=user_table):
                user = self.user_mapper.to_model(user_table)
                role_tables = UserRoleTableData.get_roles_from_user(user_table)
                self.assertEqual(user.id, str(user_table.id))
                self.assertEqual(user.name, user_table.username)
                self.assertEqual(user.email, user_table.email)
                self.assertEqual(user.password, user_table.password)
                self.assertEqual(user.roles, [self.role_mapper.to_model(role) for role in role_tables])
                self.assertEqual(user.created_date, user_table.created_date)
                self.assertEqual(user.gender, user_table.gender)
                self.assertEqual(user.birthdate, user_table.birthdate)
                self.assertEqual(user.status, user_table.status)
    
    def test_to_table(self) -> None:
        for user in DataFactory.generate_user_accounts():
            with self.subTest(user=user):
                user_table = self.user_mapper.to_table(user)
                self.assertEqual(str(user_table.id), user.id)
                self.assertEqual(user_table.name, user.name)
                self.assertEqual(user_table.email, user.email)
                self.assertEqual(user_table.password, user.password)
                self.assertEqual(user_table.created_date, user.created_date)
                self.assertEqual(user_table.birthdate, user.birthdate)
                self.assertEqual(user_table.status, user.status.value)
                self.assertEqual(user_table.gender, user.gender.value)
                self.assertEqual(user_table.phone_number, user.phone_number)
    
    
class TestRoleTableMapper(TestCase):
    role_mapper: RoleTableMapper
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.role_mapper = RoleTableMapper()
    
    def test_to_role(self) -> None:
        for role_table in DataFactory.generate_role_tables():
            role_table.save()
            with self.subTest(role_table=role_table):
                role = self.role_mapper.to_model(role_table)
                self.assertEqual(role.id, str(role_table.id))
                self.assertEqual(role.name, role_table.name)
                self.assertEqual(role.created_date, role_table.created_date)
    
    def test_to_table(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                role_table = self.role_mapper.to_table(role)
                self.assertEqual(str(role_table.id), role.id)
                self.assertEqual(role_table.name, role.name)
                self.assertEqual(role_table.created_date, role.created_date)