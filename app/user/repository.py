from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.user import UserAccount, Role
from core.user.domain.values import UserEmail, UserPhoneNumber
from core.common import EventSubscriber, Event, ID, SystemException
from core.user.service.repository import GetUser
from core.user.domain.events import (UserAccountSaved, RoleSaved, RoleAddedToUser,
                                     RoleRemovedFromUser, RoleDeleted, PhotoAddedToEmployee)
from app.common.exceptions import ModelNotFoundException
from .models import UserAccountTableData, RoleTableData, EmployeeAccountTableData, EmployeeRoleTableData, RolPermissionTableData
from .mapper import UserTableMapper, RoleTableMapper
from typing import Dict, Optional, List
from core.common import OrdenDirection

class DjangoGetUser(DjangoGetModel[UserAccountTableData, UserAccount], GetUser):
    def __init__(self) -> None:
        super().__init__(UserAccountTableData, UserTableMapper())
        self.allowed_fields = ['name', 'email', 'status', 'gender', 'birthdate',
                               'phone_number', 'created_date']
    
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
        if isinstance(user, EmployeeAccountTableData) and self.exists_employee_by_dni(user.dni): return False
        return True
    
    def get(self, unique: str) -> UserAccount:
        if UserEmail.is_email(unique):
            return self.get_by_email(unique)
        if UserPhoneNumber.is_phone_number(unique):
            return self.get_by_phone_number(unique)
        if self.exists_employee_by_id(unique):
            table = EmployeeAccountTableData.objects.get(id=unique)
            return self.mapper.to_model(table)
        return super().get(unique)
    
    def get_by_email(self, email: str) -> UserAccount:
        if not self.exists_by_email(email):
            raise ModelNotFoundException.not_found(email)
        if self.exists_employee_by_email(email):
            table = EmployeeAccountTableData.objects.get(email=email.lower())
            return self.mapper.to_model(table)
        table = self.table.objects.get(email=email.lower())
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
    
    def exists_super_admin(self) -> bool:
        return EmployeeRoleTableData.objects.filter(role__name=Role.SUPER_ADMIN).exists()
    
    def exists_employee_by_id(self, employee_id: str) -> bool:
        if not ID.is_id(employee_id): return False
        return EmployeeAccountTableData.objects.filter(id=employee_id).exists()
    
    def exists_employee_by_email(self, email: str) -> bool:
        return EmployeeAccountTableData.objects.filter(email=email.lower()).exists()
    
    def exists_employee_by_phone_number(self, phone_number: str) -> bool:
        return EmployeeAccountTableData.objects.filter(phone_number=phone_number).exists()
    
    def exists_employee_by_dni(self, dni: str) -> bool:
        return EmployeeAccountTableData.objects.filter(dni=dni).exists()
    
    def filter(self, order_by: str, direction: OrdenDirection,
               limit: Optional[int]=None, offset: Optional[int]=None,
               fields: Dict[str, str]={}) -> List[UserAccount]:
        return super().filter(order_by, direction, limit, offset, fields)
    
    def get_by_role(self, role: str) -> List[UserAccount]:
        tables = EmployeeRoleTableData.get_employees_from_role(role)
        return [self.mapper.to_model(table) for table in tables]
    

class DjangoSaveUser(DjangoSaveModel[UserAccountTableData, UserAccount], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(UserTableMapper())
        EventSubscriber.__init__(self)
        self.get_user = DjangoGetUser()
    
    def save(self, user: UserAccount) -> None:
        if not self.get_user.is_unique_user(user):
            raise UserAlreadyExistsException.already_exists(user.id)
        super().save(user)
    
    def update(self, user: UserAccount) -> None:
        if not self.get_user.exists_by_id(user.id):
            raise ModelNotFoundException.not_found(user.id)
        old_user = self.get_user.get(user.id)
        if old_user.phone_number != user.phone_number and self.get_user.exists_by_phone_number(user.phone_number):
            raise UserAlreadyExistsException.already_exists(user.phone_number)
        if old_user.email != user.email and self.get_user.exists_by_email(user.email):
            raise UserAlreadyExistsException.already_exists(user.email)
        super().save(user)
        
    def save_employee_photo(self, employee_id: str, photo: str) -> None:
        EmployeeAccountTableData.objects.filter(id=employee_id).update(photo=photo)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, UserAccountSaved):
            if event.update: self.update(event.user)
            else: self.save(event.user)
        if isinstance(event, PhotoAddedToEmployee):
            self.save_employee_photo(event.employee_id, event.photo.get_url())

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
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleDeleted):
            self.delete(event.rolename)
     
            
class RoleToUserSubscriber(EventSubscriber):
    def add_role(self, user_id: str, role: str) -> None:
        employee_table = EmployeeAccountTableData.objects.get(id=user_id)
        role_table = RoleTableData.objects.get(name=role.lower())
        EmployeeRoleTableData.objects.create(employee=employee_table, role=role_table)
    
    def remove_role(self, user_id: str, role: str) -> None:
        employee_table = EmployeeAccountTableData.objects.get(id=user_id)
        role_table = RoleTableData.objects.get(name=role)
        EmployeeRoleTableData.objects.get(employee=employee_table, role=role_table).delete()
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleAddedToUser):
            self.add_role(event.user_id, event.rolename)
        
        if isinstance(event, RoleRemovedFromUser):
            self.remove_role(event.user_id, event.rolename)


class UserAlreadyExistsException(SystemException):
    @classmethod
    def already_exists(cls, unique: str) -> "UserAlreadyExistsException":
        return cls(f'El usuario {unique} ya está registrado')


class RoleAlreadyExistsException(SystemException):
    @classmethod
    def already_exists(cls, rolename: str) -> "RoleAlreadyExistsException":
        return cls(f'El rol {rolename} ya está registrado')