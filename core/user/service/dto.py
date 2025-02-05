from pydantic import BaseModel
from datetime import date
from core.user import AccountStatus
from core.common import OrdenDirection
from typing import List, Optional

class SignUpDto(BaseModel):
    phone_number: str
    email: str
    name: str
    password: str
    birthdate: date
    roles: List[str]


class UpdateUserDto(BaseModel):
    id: str
    phone_number: str
    email: str
    name: str
    password: str
    status: AccountStatus


class FilterUserDto(BaseModel):
    expresion: Optional[str]
    order_by: str
    offset: Optional[int]
    limit: Optional[int]
    order_direction: Optional[OrdenDirection] = OrdenDirection.DESC


class RoleDto(BaseModel):
    id: str
    name: str
    created_date: date
    
    
class UserDto(BaseModel):
    id: str
    phone_number: str
    email: str
    name: str
    status: AccountStatus
    birthdate: date
    created_date: date
    roles: List[RoleDto]