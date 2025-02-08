from __future__ import annotations
from core.common import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserAccount
    from .role import Role

class UserAccountSaved(Event):
    '''Evento para cuando un usuario es actualizado'''
    def __init__(self, user: UserAccount):
        self.user = user

class RoleSaved(Event):
    '''Evento para cuando un rol es actualizado'''
    def __init__(self, role: Role):
        self.role = role

class RoleDeleted(Event):
    '''Evento para cuando un rol es eliminado'''
    def __init__(self, rolename: str):
        self.rolename = rolename

class RoleAddedToUser(Event):
    '''Evento para cuando un rol es añadido a un usuario'''
    def __init__(self, rolename: str, user_id: str):
        self.rolename = rolename
        self.user_id = user_id

class RoleRemovedFromUser(Event):
    '''Evento para cuando un rol es removido de un usuario'''
    def __init__(self, rolename: str, user_id: str):
        self.rolename = rolename
        self.user_id = user_id