from __future__ import annotations
from core.common import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserAccount
    from .role import Role

class UserAccountSaved(Event):
    '''Evento para cuando un usuario es actualizado'''
    def __init__(self, user: UserAccount, update: bool=False):
        self.user = user
        self.update = update

class RoleSaved(Event):
    '''Evento para cuando un rol es actualizado'''
    def __init__(self, role: Role, update: bool=False):
        self.role = role
        self.update = update

class RoleDeleted(Event):
    '''Evento para cuando un rol es eliminado'''
    def __init__(self, rolename: str):
        self.rolename = rolename