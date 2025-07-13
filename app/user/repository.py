from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.user import UserAccount, Role, EmployeeAccount
from core.user.domain.values import UserEmail, UserPhoneNumber, EmployeeCategories
from core.common import EventSubscriber, Event, ID, SystemException
from core.user.service.repository import GetUser
from core.user.domain.events import (UserAccountSaved, RoleSaved, RoleDeleted)
from app.common.exceptions import ModelNotFoundException
from .models import UserAccountTableData, RoleTableData, EmployeeAccountTableData, EmployeeRoleTableData, RolPermissionTableData, EmployeeCategoriesTableData
from .mapper import UserTableMapper, RoleTableMapper
from typing import List, Tuple
from django.db.models import Q
from core.user.service.dto import FilterUserDto

class DjangoGetUser(DjangoGetModel[UserAccountTableData, UserAccount], GetUser):
    def __init__(self) -> None:
        super().__init__(UserAccountTableData, UserTableMapper())
    
    def exists(self, unique: str) -> bool:
        if UserEmail.is_email(unique):
            return self.exists_by_email(unique)
        if UserPhoneNumber.is_phone_number(unique):
            return self.exists_by_phone_number(unique)
        if ID.is_id(unique):
            return super().exists(unique)
        return False
    
    def is_unique_user(self, user: UserAccount) -> bool:
        if self.exists_by_email(user.email): return False
        if self.exists_by_phone_number(user.phone_number): return False
        if self.exists(user.id): return False
        if self.exists_by_dni(user.dni): return False
        return True
    
    def get(self, unique: str) -> UserAccount:
        if UserEmail.is_email(unique):
            return self.get_by_email(unique)
        if UserPhoneNumber.is_phone_number(unique):
            return self.get_by_phone_number(unique)
        if self.exists_by_dni(unique):
            table = UserAccountTableData.objects.get(id=unique)
            return self.mapper.to_model(table)
        return self.get_by_id(unique)
    
    def get_by_email(self, email: str) -> UserAccount:
        if not self.exists_by_email(email):
            raise ModelNotFoundException.not_found(email)
        if self.exists_employee_by_email(email):
            table = EmployeeAccountTableData.objects.get(email=email.lower())
            return self.mapper.to_model(table)
        table = self.table.objects.get(email=email.lower())
        return self.mapper.to_model(table)

    def get_by_id(self, user_id: str) -> UserAccount:
        if not self.exists_by_id(user_id):
            raise ModelNotFoundException.not_found(user_id)
        if self.exists_employee_by_id(user_id):
            table = EmployeeAccountTableData.objects.get(id=user_id)
            return self.mapper.to_model(table)
        table = self.table.objects.get(id=user_id)
        return self.mapper.to_model(table)
    
    def get_by_phone_number(self, phone_number: str) -> UserAccount:
        if not self.exists_by_phone_number(phone_number):
            raise ModelNotFoundException.not_found(phone_number)
        if self.exists_employee_by_phone_number(phone_number):
            table = EmployeeAccountTableData.objects.get(phone_number=phone_number)
            return self.mapper.to_model(table)
        table = self.table.objects.get(phone_number=phone_number)
        return self.mapper.to_model(table)
    
    def exists_by_phone_number(self, phone_number: str) -> bool:
        return self.table.objects.filter(phone_number=phone_number).exists()
    
    def exists_by_email(self, email: str) -> bool:
        return self.table.objects.filter(email=email.lower()).exists()
    
    def exists_by_id(self, user_id: str) -> bool:
        return super().exists(user_id)
    
    def exists_by_dni(self, dni: str) -> bool:
        return self.table.objects.filter(dni=dni).exists()
    
    def exists_super_admin(self) -> bool:
        return EmployeeRoleTableData.objects.filter(role__name=Role.SUPER_ADMIN).exists()
    
    def exists_employee_by_id(self, employee_id: str) -> bool:
        if not ID.is_id(str(employee_id)): return False
        return EmployeeAccountTableData.objects.filter(id=employee_id).exists()
    
    def exists_employee_by_email(self, email: str) -> bool:
        return EmployeeAccountTableData.objects.filter(email=email.lower()).exists()
    
    def exists_employee_by_phone_number(self, phone_number: str) -> bool:
        return EmployeeAccountTableData.objects.filter(phone_number=phone_number).exists()
    
    def get_by_role(self, role: str) -> List[UserAccount]:
        tables = EmployeeRoleTableData.get_employees_from_role(role)
        return [self.mapper.to_model(table) for table in tables]
    
    def get_all(self) -> List[UserAccount]:
        tables = self.table.objects.all()
        return [self.get(str(table.id)) for table in tables]
    
    def build_filter(self, filter_data: FilterUserDto) -> Q:
        _filter = Q()
        if filter_data.service_category:
            _filter &= Q(employeeaccounttabledata__employeecategoriestabledata__category=filter_data.service_category.value.upper())
        if filter_data.only_clients:
            _filter &= ~Q(id__in=EmployeeAccountTableData.objects.values_list('id', flat=True))
        if filter_data.name:
            _filter &= Q(name__icontains=filter_data.name.lower())
        elif filter_data.exact_name:
            _filter &= Q(name__iexact=filter_data.exact_name.lower())
        if filter_data.role:
            _filter &= Q(employeeaccounttabledata__employeeroletabledata__role__name=filter_data.role.lower())
        if filter_data.email:
            _filter &= Q(email__icontains=filter_data.email.lower())
        if filter_data.phone_number:
            _filter &= Q(phone_number__icontains=filter_data.phone_number)
        if filter_data.dni:
            _filter &= Q(dni__icontains=filter_data.dni)
        return _filter
            
    def get_filtered_users(self, filter_data: FilterUserDto) -> Tuple[List[UserAccount], int]:
        _filter = self.build_filter(filter_data)
        user_tables = self.table.objects.filter(_filter).distinct()
        tables_count =user_tables.count()
        if filter_data.only_count: return [], tables_count
        if filter_data.limit and filter_data.offset:
            user_tables = user_tables[filter_data.offset:filter_data.offset + filter_data.limit]
        elif filter_data.limit:
            user_tables = user_tables[:filter_data.limit]
        elif filter_data.offset:
            user_tables = user_tables[filter_data.offset:]
        models : List[UserAccount] = []
        for table in user_tables:
            if self.exists_employee_by_id(table.id):
                models.append(self.mapper.to_model(EmployeeAccountTableData.objects.get(id=table.id)))
            else:
                models.append(self.mapper.to_model(table))
        return models, tables_count
    

class DjangoSaveUser(DjangoSaveModel[UserAccountTableData, UserAccount], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(UserTableMapper())
        EventSubscriber.__init__(self)
        self.get_user = DjangoGetUser()
    
    def save(self, user: UserAccount) -> None:
        if not self.get_user.is_unique_user(user):
            raise UserAlreadyExistsException.already_exists(user.id)
        super().save(user)
        if isinstance(user, EmployeeAccount):
            self.save_categories(user.id, user.categories)
            self.save_roles(user.id, user.roles)

    def save_roles(self, employee_id: str, roles: List[str]) -> None:
        employee = EmployeeAccountTableData.objects.get(id=employee_id)
        EmployeeRoleTableData.objects.filter(employee=employee).delete()
        for role in roles:
            EmployeeRoleTableData.objects.create(employee=employee,
                                                 role=RoleTableData.objects.get(name=role.lower())
                                                 )
        if 'MOVIL' not in RolPermissionTableData.get_access_from_user(employee_id):
            EmployeeCategoriesTableData.objects.filter(employee=employee).delete()
    
    def save_categories(self, employee_id: str, categories: List[EmployeeCategories]) -> None:
        employee = EmployeeAccountTableData.objects.get(id=employee_id)
        EmployeeCategoriesTableData.objects.filter(employee=employee).delete()
        for category in categories:
            EmployeeCategoriesTableData.objects.create(employee=employee, category=category.value)
        
    def update(self, user: UserAccount) -> None:
        if not self.get_user.exists_by_id(user.id):
            raise ModelNotFoundException.not_found(user.id)
        old_user = self.get_user.get(user.id)
        if old_user.phone_number != user.phone_number and self.get_user.exists_by_phone_number(user.phone_number):
            raise UserAlreadyExistsException.already_exists(user.phone_number)
        if old_user.email != user.email and self.get_user.exists_by_email(user.email):
            raise UserAlreadyExistsException.already_exists(user.email)
        if old_user.dni != user.dni and self.get_user.exists_by_dni(user.dni):
            raise UserAlreadyExistsException.already_exists(user.dni)
        if isinstance(user, EmployeeAccount) and isinstance(old_user, EmployeeAccount):
            self.save_categories(user.id, user.categories)
            self.save_roles(user.id, user.roles)
        super().save(user)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, UserAccountSaved):
            if event.update: self.update(event.user)
            else: self.save(event.user)


class DjangoGetRole(DjangoGetModel[RoleTableData, Role]):
    def __init__(self) -> None:
        super().__init__(RoleTableData, RoleTableMapper())
        
    def exists(self, rolename: str) -> bool:
        if ID.is_id(rolename):
            return super().exists(rolename)
        return self.exists_by_name(rolename)
    
    def is_unique_role(self, role: Role) -> bool:
        if self.exists(role.id): return False
        if self.exists_by_name(role.name): return False
        return True
    
    def exists_by_name(self, rolename: str) -> bool:
        return self.table.objects.filter(name=rolename.lower()).exists()
    
    def get(self, unique: str) -> Role:
        if ID.is_id(unique):
            return super().get(unique)
        return self.get_by_name(unique)
    
    def get_by_name(self, rolename: str) -> Role:
        if not self.exists_by_name(rolename):
            raise ModelNotFoundException.not_found(rolename)
        table = self.table.objects.get(name=rolename.lower())
        return self.mapper.to_model(table)
    
class DjangoSaveRole(DjangoSaveModel[RoleTableData, Role], EventSubscriber):    
    def __init__(self) -> None:
        super().__init__(RoleTableMapper())
        EventSubscriber.__init__(self)
        self.get_role = DjangoGetRole()
    
    def save(self, role: Role) -> None:
        if not self.get_role.is_unique_role(role):
            raise RoleAlreadyExistsException.already_exists(role.name)
        super().save(role)
        self.save_accesses(role)
    
    def update(self, role: Role) -> None:
        if not self.get_role.exists(role.id):
            raise ModelNotFoundException.not_found(role.id)
        old_role = self.get_role.get(role.id)
        if old_role.name != role.name and self.get_role.exists_by_name(role.name):
            raise RoleAlreadyExistsException.already_exists(role.name)
        super().save(role)
        self.update_accesses(role)
    
    def save_accesses(self, role: Role) -> None:
        for access in role.accesses:
            for permission in access.permissions:
                RolPermissionTableData.objects.create(
                    role = RoleTableData.objects.get(name=role.name),
                    access = access.access_type.value,
                    permission = permission.value
                )
    
    def update_accesses(self, role: Role) -> None:
        RolPermissionTableData.objects.filter(role=role.id).delete()
        self.save_accesses(role)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleSaved):
            if event.update: self.update(event.role)
            else: self.save(event.role)


class DjangoDeleteRole(DjangoDeleteModel[RoleTableData, Role], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(RoleTableData, RoleTableMapper(), DjangoGetRole())
        EventSubscriber.__init__(self)
    
    def delete(self, id: str) -> Role:
        employee_tables = EmployeeRoleTableData.get_employees_from_role(id)
        role = super().delete(id)
        for employee in employee_tables:
            employee_accesses = RolPermissionTableData.get_access_from_user(employee.id)
            if 'MOVIL' not in employee_accesses:
                EmployeeCategoriesTableData.objects.filter(employee=employee).delete()
        return role
        
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleDeleted):
            self.delete(event.rolename)


class UserAlreadyExistsException(SystemException):
    @classmethod
    def already_exists(cls, unique: str) -> "UserAlreadyExistsException":
        return cls(f'El usuario {unique} ya está registrado')


class RoleAlreadyExistsException(SystemException):
    @classmethod
    def already_exists(cls, rolename: str) -> "RoleAlreadyExistsException":
        return cls(f'El rol {rolename} ya está registrado')