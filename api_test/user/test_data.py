from core_test.user.test_data import DataFactory as CoreDataFactory
from app.user.models import UserAccountTableData, RoleTableData
from core.common import ID
from typing import List

class DataFactory(CoreDataFactory):
    @classmethod
    def generate_user_tables(cls) -> List[UserAccountTableData]:
        users = cls.generate_user_accounts()
        return [
            UserAccountTableData(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                phone_number=user.phone_number,
                birthdate=user.birthdate,
                status=user.status,
                gender=user.gender,
                created_date=user.created_date,
            ) for user in users
        ]
    
    @classmethod
    def generate_role_tables(cls) -> List[RoleTableData]:
        return [
            RoleTableData(
                id=ID.generate(),
                name=role_name.lower(),
                created_date=cls.user_test_data.get_created_date(),
            ) for role_name in cls.user_test_data.get_roles()
        ]