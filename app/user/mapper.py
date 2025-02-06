from app.common.table_mapper import TableMapper
from .models import UserAccountTableData, RoleTableData, UserRoleTableData
from core.user import UserAccount, Role, UserAccountFactory, RoleFactory

class UserTableMapper(TableMapper[UserAccountTableData, UserAccount]):
    def to_model(self, user_table: UserAccountTableData) -> UserAccount:
        #TODO
        user: UserAccount
        return user
    
    def to_table(self, user: UserAccount) -> UserAccountTableData:
        #TODO
        user_table: UserAccountTableData
        return user_table


class RoleTableMapper(TableMapper[RoleTableData, Role]):
    def to_model(self, role_table: RoleTableData) -> Role:
        #TODO
        role: Role
        return role
    
    def to_table(self, role: Role) -> RoleTableData:
        #TODO
        role_table: RoleTableData
        return role_table