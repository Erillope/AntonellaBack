from pydantic import BaseModel
from datetime import date
from core.user import AccountStatus, Gender
from core.user.domain.values import RoleAccess, EmployeeCategories, PaymentType
from core.common import OrdenDirection
from typing import List, Optional, Dict, Any

class SignUpDto(BaseModel):
    phone_number: str
    email: str
    name: str
    gender: Gender
    password: str
    birthdate: date
    dni: str
    photo: Optional[str] = None


class CreateEmployeeDto(SignUpDto):
    address: str
    roles: List[str]
    categories: List[EmployeeCategories] = []
    payment_type: PaymentType


class UpdateUserDto(BaseModel):
    id: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    status: Optional[AccountStatus] = None
    dni: Optional[str] = None
    address: Optional[str] = None
    photo: Optional[str] = None
    roles: Optional[List[str]] = None
    birthdate: Optional[date] = None
    gender: Optional[Gender] = None
    categories: Optional[List[EmployeeCategories]] = None
    payment_type: Optional[PaymentType] = None


class FilterUserDto(BaseModel):
    fields : Dict[str, str] = {}
    order_by: str
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_direction: OrdenDirection = OrdenDirection.DESC


class RoleDto(BaseModel):
    id: str
    name: str
    accesses: List[RoleAccess]
    created_date: date
    
    def role_dump(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        for access in data['accesses']:
            value = access.pop('access_type')
            access['access'] = value
        return data
    
class UserDto(BaseModel):
    id: str
    dni: str
    address: Optional[str] = None
    photo: Optional[str] = None
    payment_type: Optional[PaymentType] = None
    phone_number: str
    email: str
    name: str
    status: AccountStatus
    gender: Gender
    birthdate: date
    created_date: date
    roles: List[str] = []
    categories: List[EmployeeCategories] = []
    
    def user_dump(self) -> Dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        if not self.roles:
            data.pop('roles')
        if not self.categories:
            data.pop('categories')
        return data