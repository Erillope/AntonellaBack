from __future__ import annotations
from core.common import Event
from pydantic import BaseModel
from typing import TYPE_CHECKING
from datetime import date
if TYPE_CHECKING:
    from .user import UserAccount
    from .role import Role

class UserAccountCreated(Event, BaseModel):
    '''Evento para cuando un usuario es creado'''
    user: UserAccount

class UserAccountUpdated(Event, BaseModel):
    '''Evento para cuando un usuario es actualizado'''
    user: UserAccount

class RoleCreated(Event, BaseModel):
    '''Evento para cuando un rol es creado'''
    role: Role

class RoleUpdated(Event, BaseModel):
    '''Evento para cuando un rol es actualizado'''
    role: Role

class RoleAddedToUser(Event, BaseModel):
    '''Evento para cuando un rol es añadido a un usuario'''
    role_id: str
    user_id: str

class RoleRemovedFromUser(Event, BaseModel):
    '''Evento para cuando un rol es removido de un usuario'''
    role_id: str
    user_id: str