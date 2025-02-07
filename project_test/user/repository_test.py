from django.test import TestCase
from app.user.repository import DjangoSaveModel, DjangoSaveRole, DjangoSaveUser, RoleToUserSubscriber
from app.common.django_repository import DjangoGetModel, DjangoDeleteModel
from app.common.exceptions import ModelNotFoundException
from app.user.models import UserAccountTableData, RoleTableData
from app.user.mapper import UserTableMapper, RoleTableMapper
from core.user import UserAccount, Role
from .test_data import DataFactory

class UserRepositoryTest(TestCase):
    get_user: DjangoGetModel[UserAccountTableData, UserAccount]
    save_user: DjangoSaveUser
    user_mapper: UserTableMapper
    created_users: list[UserAccountTableData]
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.user_mapper = UserTableMapper()
        cls.get_user = DjangoGetModel[UserAccountTableData, UserAccount](
            UserAccountTableData,
            cls.user_mapper
        )
        cls.save_user = DjangoSaveUser()
        cls.created_users = DataFactory.generate_user_tables()
        for user in cls.created_users:
            user.save()
    
    def test_exists_user(self) -> None:
        for user in self.created_users:
            with self.subTest(user=user):
                self.assertTrue(self.get_user.exists(user.id))
                self.assertTrue(self.get_user.exists(user.phone_number))
                self.assertTrue(self.get_user.exists(user.email))
    
    def test_get_user(self) -> None:
        for user in self.created_users:
            with self.subTest(user=user):
                user_model = self.user_mapper.to_model(user)
                self.assertEqual(self.get_user.get(user.id), user_model)
                self.assertEqual(self.get_user.get(user.phone_number), user_model)
                self.assertEqual(self.get_user.get(user.email), user_model)
    
    def test_not_found_user(self) -> None:
        for id in DataFactory.user_test_data.get_invalid_ids():
            with self.subTest(id=id):
                with self.assertRaises(ModelNotFoundException):
                    self.get_user.get(id)
    
    def test_save_user(self) -> None:
        for user in DataFactory.generate_user_accounts():
            with self.subTest(user=user):
                self.save_user.save(user)
                saved_user = self.get_user.get(user.id)
                self.assertEqual(user, saved_user)


class RoleRepositoryTest(TestCase):
    get_role: DjangoGetModel[RoleTableData, Role]
    save_role: DjangoSaveRole
    delete_role: DjangoDeleteModel[RoleTableData]
    role_mapper: RoleTableMapper
    created_roles: list[RoleTableData]
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.role_mapper = RoleTableMapper()
        cls.get_role = DjangoGetModel[RoleTableData, Role](
            RoleTableData,
            cls.role_mapper
        )
        cls.save_role = DjangoSaveRole()
        cls.delete_role = DjangoDeleteModel[RoleTableData](
            RoleTableData(),
            cls.role_mapper
        )
        cls.created_roles = DataFactory.generate_role_tables()
        for role in cls.created_roles:
            role.save()
    
    def test_exists_role(self) -> None:
        for role in self.created_roles:
            with self.subTest(role=role):
                self.assertTrue(self.get_role.exists(role.id))
                self.assertTrue(self.get_role.exists(role.name))
    
    def test_get_role(self) -> None:
        for role in self.created_roles:
            with self.subTest(role=role):
                role_model = self.role_mapper.to_model(role)
                self.assertEqual(self.get_role.get(role.id), role_model)
                self.assertEqual(self.get_role.get(role.name), role_model)
    
    def test_not_found_role(self) -> None:
        for id in DataFactory.role_test_data.get_invalid_ids():
            with self.subTest(id=id):
                with self.assertRaises(ModelNotFoundException):
                    self.get_role.get(id)
    
    def test_save_role(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                self.save_role.save(role)
                saved_role = self.get_role.get(role.id)
                self.assertEqual(role, saved_role)
    
    def test_delete_role(self) -> None:
        for role in DataFactory.generate_roles():
            with self.subTest(role=role):
                self.save_role.save(role)
                self.delete_role.delete(role.id)
                self.assertNotTrue(self.get_role.exists(role.id))