from app.common.table_mapper import TableMapper
from .models import UserAccountTableData, RoleTableData, EmployeeRoleTableData, EmployeeAccountTableData, RolPermissionTableData, EmployeeCategoriesTableData
from core.user import UserAccount, Role, UserAccountFactory, RoleFactory, AccountStatus, Gender, EmployeeAccount
from core.user.domain.values import AccessType, PermissionType, EmployeeCategories, PaymentType

class UserTableMapper(TableMapper[UserAccountTableData, UserAccount]):
    def __init__(self) -> None:
        self.role_mapper = RoleTableMapper()
        
    def to_model(self, user_table: UserAccountTableData) -> UserAccount:
        if isinstance(user_table, EmployeeAccountTableData):
            return self._to_employee(user_table)
        return self._to_user(user_table)
    
    def to_table(self, user: UserAccount) -> UserAccountTableData:
        if isinstance(user, EmployeeAccount):
            return self._from_employee_user(user)
        return self._from_client_user(user)
    
    def _to_user(self, user_table: UserAccountTableData) -> UserAccount:
        return UserAccountFactory.load_user(
            id=str(user_table.id),
            name=user_table.name,
            email=user_table.email,
            password=user_table.password,
            phone_number=user_table.phone_number,
            birthdate=user_table.birthdate,
            status=AccountStatus(user_table.status.upper()),
            gender=Gender(user_table.gender.upper()),
            created_date=user_table.created_date,
            dni=user_table.dni,
            photo=user_table.photo
        )
    
    def _to_employee(self, user_table: EmployeeAccountTableData) -> EmployeeAccount:
        return UserAccountFactory.load_employee(
            id=str(user_table.id),
            name=user_table.name,
            email=user_table.email,
            password=user_table.password,
            phone_number=user_table.phone_number,
            birthdate=user_table.birthdate,
            status=AccountStatus(user_table.status.upper()),
            gender=Gender(user_table.gender.upper()),
            created_date=user_table.created_date,
            dni=user_table.dni,
            address=user_table.address,
            photo=user_table.photo,
            roles=[
                role.name for role in EmployeeRoleTableData.get_roles_from_employee(user_table.id)
            ],
            categories= [
                EmployeeCategories(category) for category in EmployeeCategoriesTableData.get_categories_from_employee(user_table.id)
            ],
            payment_type = PaymentType(user_table.payment_type.upper())
        )
    
    def _from_client_user(self, user: UserAccount) -> UserAccountTableData:
        return UserAccountTableData(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            phone_number=user.phone_number,
            birthdate=user.birthdate,
            status=user.status.value.lower(),
            gender=user.gender.value.lower(),
            created_date=user.created_date,
            dni=user.dni,
            photo=user.photo
        )
    
    def _from_employee_user(self, user: EmployeeAccount) -> EmployeeAccountTableData:
        return EmployeeAccountTableData(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            phone_number=user.phone_number,
            birthdate=user.birthdate,
            status=user.status.value.lower(),
            gender=user.gender.value.lower(),
            created_date=user.created_date,
            dni=user.dni,
            address=user.address,
            photo=user.photo,
            payment_type=user.payment_type.value.lower(),
        )


class RoleTableMapper(TableMapper[RoleTableData, Role]):
    def to_model(self, role_table: RoleTableData) -> Role:
        role =  RoleFactory.load(
            id=str(role_table.id),
            name=role_table.name,
            accesses=set(),
            created_date=role_table.created_date
        )
        for role_access in RolPermissionTableData.get_permissions_from_role(role_table.id):
            role.add_access(
                access_type=AccessType(role_access.access.upper()),
                permission=PermissionType(role_access.permission.upper())
            )
        return role
    
    def to_table(self, role: Role) -> RoleTableData:
        return RoleTableData(
            id=role.id,
            name=role.name,
            created_date=role.created_date
        )