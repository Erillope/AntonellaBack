from app.common.table_mapper import TableMapper
from .models import UserAccountTableData, RoleTableData, UserRoleTableData
from core.user import UserAccount, Role, UserAccountFactory, RoleFactory, AccountStatus, Gender

class UserTableMapper(TableMapper[UserAccountTableData, UserAccount]):
    def __init__(self) -> None:
        self.role_mapper = RoleTableMapper()
        
    def to_model(self, user_table: UserAccountTableData) -> UserAccount:
        return UserAccountFactory.load(
            id=str(user_table.id),
            name=user_table.name,
            email=user_table.email,
            password=user_table.password,
            phone_number=user_table.phone_number,
            birthdate=user_table.birthdate,
            status=AccountStatus(user_table.status),
            gender=Gender(user_table.gender),
            created_date=user_table.created_date,
            roles=[self.role_mapper.to_model(role_table) 
                   for role_table in UserRoleTableData.get_roles_from_user(user_table)]
        )
    
    def to_table(self, user: UserAccount) -> UserAccountTableData:
        return UserAccountTableData(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            phone_number=user.phone_number,
            birthdate=user.birthdate,
            status=user.status.value,
            gender=user.gender.value,
            created_date=user.created_date
        )


class RoleTableMapper(TableMapper[RoleTableData, Role]):
    def to_model(self, role_table: RoleTableData) -> Role:
        return RoleFactory.load(
            id=str(role_table.id),
            name=role_table.name,
            created_date=role_table.created_date
        )
    
    def to_table(self, role: Role) -> RoleTableData:
        return RoleTableData(
            id=role.id,
            name=role.name,
            created_date=role.created_date
        )