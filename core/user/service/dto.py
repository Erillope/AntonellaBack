from pydantic import BaseModel
from datetime import date
from core.user import AccountStatus, Gender
from core.common import OrdenDirection
from typing import List, Optional

class SignUpDto(BaseModel):
    phone_number: str
    email: str
    name: str
    gender: Gender
    password: str
    birthdate: date
    roles: List[str] = []


class UpdateUserDto(BaseModel):
    id: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    status: Optional[AccountStatus] = None


class FilterUserDto(BaseModel):
    expresion: Optional[str] = None
    order_by: str
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_direction: OrdenDirection = OrdenDirection.DESC


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
    gender: Gender
    birthdate: date
    created_date: date
    roles: List[RoleDto]