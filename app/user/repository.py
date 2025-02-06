from app.common.django_repository import DjangoSaveModel
from core.user import UserAccount, Role
from core.common import EventSubscriber, Event
from core.user.domain.events import (UserAccountCreated, UserAccountUpdated, RoleCreated, RoleUpdated,
                                     RoleAddedToUser, RoleRemovedFromUser)
from .models import UserAccountTableData, RoleTableData, UserRoleTableData
from .mapper import UserTableMapper, RoleTableMapper

class DjangoSaveUser(DjangoSaveModel[UserAccountTableData, UserAccount], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(UserTableMapper())
    
    def handle(self, event: Event) -> None:
        if isinstance(event, UserAccountCreated):
            self.save(event.user)
        elif isinstance(event, UserAccountUpdated):
            self.save(event.user)


class DjangoSaveRole(DjangoSaveModel[RoleTableData, Role], EventSubscriber):    
    def __init__(self) -> None:
        super().__init__(RoleTableMapper())
    
    def handle(self, event: Event) -> None:
        if isinstance(event, RoleCreated):
            self.save(event.role)
        elif isinstance(event, RoleUpdated):
            self.save(event.role)


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