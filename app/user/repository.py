from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel
from core.user import UserAccount, Role
from core.common import EventSubscriber, Event, EventPublisher
from core.user.domain.events import (UserAccountSaved, RoleSaved, RoleAddedToUser,
                                     RoleRemovedFromUser, RoleDeleted)
from .models import UserAccountTableData, RoleTableData, UserRoleTableData
from .mapper import UserTableMapper, RoleTableMapper

class DjangoSaveUser(DjangoSaveModel[UserAccountTableData, UserAccount], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(UserTableMapper())
    
    def handle(self, event: Event) -> None:
        if isinstance(event, UserAccountSaved):
            self.save(event.user)


class DjangoSaveRole(DjangoSaveModel[RoleTableData, Role], EventSubscriber):    
    def __init__(self) -> None:
        super().__init__(RoleTableMapper())
        EventPublisher.subscribe(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleSaved):
            self.save(event.role)


class DjangoDeleteRole(DjangoDeleteModel[RoleTableData, Role], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(RoleTableData, RoleTableMapper())
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleDeleted):
            self.delete(event.rolename)
            
class RoleToUserSubscriber(EventSubscriber):
    def add_role(self, user_id: str, role: str) -> None:
        #TODO
        return
    
    def remove_role(self, user_id: str, role: str) -> None:
        #TODO
        return
        
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleAddedToUser):
            self.add_role(event.user_id, event.rolename)
        
        if isinstance(event, RoleRemovedFromUser):
            self.remove_role(event.user_id, event.rolename)