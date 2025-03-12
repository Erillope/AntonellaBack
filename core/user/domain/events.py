from __future__ import annotations
from core.common import Event
from core.common.image_storage import ImageSaved, ImageDeleted, Base64ImageStorage
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


class PhotoAddedToEmployee(ImageSaved):
    '''Evento para cuando una foto es añadida a un empleado'''
    def __init__(self, employee_id: str, photo: Base64ImageStorage):
        super().__init__([photo])
        self.photo = photo
        self.employee_id = employee_id