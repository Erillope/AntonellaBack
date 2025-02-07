import unittest
from core.user.service.mapper import UserMapper, RoleMapper
from ..test_data import DataFactory

class TestUserMapper(unittest.TestCase):    
    def test_to_user(self) -> None:
        for sign_up_dto in DataFactory.generate_sign_up_dtos():
            with self.subTest(sign_up_dto=sign_up_dto):
                user = UserMapper.to_user(sign_up_dto)
                self.assertEqual(sign_up_dto.phone_number, user.phone_number)
                self.assertEqual(sign_up_dto.email.lower(), user.email.lower())
                self.assertEqual(sign_up_dto.name, user.name)
                self.assertTrue(user.verify_password(sign_up_dto.password))
                self.assertEqual(sign_up_dto.birthdate, user.birthdate)
                self.assertEqual([role.lower() for role in sign_up_dto.roles], [role.name for role in user.roles])
    
    def test_to_dto(self) -> None:
        for user in DataFactory.generate_user_accounts():
            with self.subTest(user=user):
                dto = UserMapper.to_dto(user)
                self.assertEqual(user.id, dto.id)
                self.assertEqual(user.phone_number, dto.phone_number)
                self.assertEqual(user.email, dto.email.lower())
                self.assertEqual(user.name, dto.name)
                self.assertEqual(user.birthdate, dto.birthdate)
                self.assertEqual(user.created_date, dto.created_date)
                self.assertEqual(user.status, dto.status)
                self.assertEqual([role.name for role in user.roles], dto.roles)

class TestRoleMapper(unittest.TestCase):
    def test_to_role(self) -> None:
        for rolename in DataFactory.user_test_data.get_roles():
            with self.subTest(rolename=rolename):
                role = RoleMapper.to_role(rolename)
                self.assertEqual(rolename.lower(), role.name.lower())
    
    def test_to_dto(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                dto = RoleMapper.to_dto(role)
                self.assertEqual(role.id, dto.id)
                self.assertEqual(role.name, dto.name.lower())
                self.assertEqual(role.created_date, dto.created_date)