from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.user import UserAccount, Role
from core.user.domain.values import UserEmail, UserPhoneNumber
from core.common import EventSubscriber, Event, ID
from core.user.domain.events import (UserAccountSaved, RoleSaved, RoleAddedToUser,
                                     RoleRemovedFromUser, RoleDeleted)
from app.common.exceptions import ModelNotFoundException
from .models import UserAccountTableData, RoleTableData, UserRoleTableData
from .mapper import UserTableMapper, RoleTableMapper

class DjangoGetUser(DjangoGetModel[UserAccountTableData, UserAccount]):
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
    
    def get(self, unique: str) -> UserAccount:
        if UserEmail.is_email(unique):
            return self.get_by_email(unique)
        if UserPhoneNumber.is_phone_number(unique):
            return self.get_by_phone_number(unique)
        return super().get(unique)
    
    def get_by_email(self, email: str) -> UserAccount:
        if not self.exists_by_email(email):
            raise ModelNotFoundException.not_found(email)
        table = self.table.objects.get(email=email.lower())
        return self.mapper.to_model(table)
    
    def get_by_phone_number(self, phone_number: str) -> UserAccount:
        if not self.exists_by_phone_number(phone_number):
            raise ModelNotFoundException.not_found(phone_number)
        table = self.table.objects.get(phone_number=phone_number)
        return self.mapper.to_model(table)
        
    def exists_by_phone_number(self, phone_number: str) -> bool:
        return self.table.objects.filter(phone_number=phone_number).exists()
    
    def exists_by_email(self, email: str) -> bool:
        return self.table.objects.filter(email=email.lower()).exists()
    
class DjangoSaveUser(DjangoSaveModel[UserAccountTableData, UserAccount], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(UserTableMapper())
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, UserAccountSaved):
            self.save(event.user)


class DjangoGetRole(DjangoGetModel[RoleTableData, Role]):
    def __init__(self) -> None:
        super().__init__(RoleTableData, RoleTableMapper())
        
    def exists(self, rolename: str) -> bool:
        return self.table.objects.filter(name=rolename.lower()).exists()
    
    def get(self, rolename: str) -> Role:
        if not self.exists(rolename):
            raise ModelNotFoundException.not_found(rolename)
        table = self.table.objects.get(name=rolename.lower())
        return self.mapper.to_model(table)
    
class DjangoSaveRole(DjangoSaveModel[RoleTableData, Role], EventSubscriber):    
    def __init__(self) -> None:
        super().__init__(RoleTableMapper())
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleSaved):
            self.save(event.role)


class DjangoDeleteRole(DjangoDeleteModel[RoleTableData, Role], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(RoleTableData, RoleTableMapper(), DjangoGetRole())
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleDeleted):
            self.delete(event.rolename)
            
class RoleToUserSubscriber(EventSubscriber):
    def add_role(self, user_id: str, role: str) -> None:
        user_table = UserAccountTableData.objects.get(id=user_id)
        role_table = RoleTableData.objects.get(name=role)
        UserRoleTableData.objects.create(user=user_table, role=role_table)
    
    def remove_role(self, user_id: str, role: str) -> None:
        user_table = UserAccountTableData.objects.get(id=user_id)
        role_table = RoleTableData.objects.get(name=role)
        UserRoleTableData.objects.get(user=user_table, role=role_table).delete()
        
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleAddedToUser):
            self.add_role(event.user_id, event.rolename)
        
        if isinstance(event, RoleRemovedFromUser):
            self.remove_role(event.user_id, event.rolename)