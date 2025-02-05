import unittest
from core.user.service.mapper import UserMapper, RoleMapper
from core.user import UserAccountFactory, RoleFactory
from core.user.service.dto import SignUpDto, UserDto
from datetime import date

class TestUserMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_sign_up_dto = SignUpDto(
            phone_number='09123456789',
            email="erick@gmail.com",
            name="Erick",
            password="Contraseña-123",
            birthdate=date(1999, 1, 1),
            roles=['ADMIN', 'USER']
        )
        
        self.sample_user = UserAccountFactory.create(
            phone_number='09123456789',
            email="erillope@gmail.com",
            name="Erick",
            password="Contraseña-123",
            birthdate=date(1999, 1, 1),
            roles=[RoleFactory.create('ADMIN'), RoleFactory.create('USER')]
        )
    
    def test_to_user(self) -> None:
        user = UserMapper.to_user(self.sample_sign_up_dto)
        self.assertEqual(self.sample_sign_up_dto.phone_number, user.phone_number)
        self.assertEqual(self.sample_sign_up_dto.email, user.email)
        self.assertEqual(self.sample_sign_up_dto.name, user.name)
        self.assertTrue(user.verify_password(self.sample_sign_up_dto.password))
        self.assertEqual(self.sample_sign_up_dto.birthdate, user.birthdate)
        self.assertEqual(self.sample_sign_up_dto.roles, [role.name for role in user.roles])
    
    def test_to_dto(self) -> None:
        dto = UserMapper.to_dto(self.sample_user)
        self.assertEqual(self.sample_user.id, dto.id)
        self.assertEqual(self.sample_user.phone_number, dto.phone_number)
        self.assertEqual(self.sample_user.email, dto.email)
        self.assertEqual(self.sample_user.name, dto.name)
        self.assertEqual(self.sample_user.birthdate, dto.birthdate)
        self.assertEqual(self.sample_user.created_date, dto.created_date)
        self.assertEqual(self.sample_user.status, dto.status)
        self.assertEqual([role.name for role in self.sample_user.roles], dto.roles)


class TestRoleMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.sample_rolename = 'ADMIN'
        self.sample_role = RoleFactory.create(self.sample_rolename)
    
    def test_to_role(self) -> None:
        role = RoleMapper.to_role(self.sample_rolename)
        self.assertEqual(self.sample_rolename, role.name)
    
    def test_to_dto(self) -> None:
        dto = RoleMapper.to_dto(self.sample_role)
        self.assertEqual(self.sample_role.name, dto.name)