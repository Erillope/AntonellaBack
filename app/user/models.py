from core.user import AccountStatus, Gender
from django.db import models #type: ignore
from typing import List, Set

class UserAccountTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    phone_number = models.CharField(max_length=250, blank=False, unique=True)
    email = models.EmailField(max_length=250, blank=False, unique=True)
    dni = models.CharField(max_length=250, blank=False, unique=True)
    name = models.CharField(max_length=25, blank=False)
    password = models.CharField(max_length=250, blank=False)
    status = models.CharField(max_length=25, choices=[(s.name, s.name) for s in AccountStatus])
    gender = models.CharField(max_length=25, choices=[(g.name, g.name) for g in Gender])
    birthdate = models.DateField(blank=False)
    created_date = models.DateField(auto_now_add=True, editable=False)
    photo = models.CharField(max_length=250, null=True)
    
    class Meta:
        db_table = "user_account"


class EmployeeAccountTableData(UserAccountTableData):
    address = models.CharField(max_length=250, blank=False)
    payment_type = models.CharField(max_length=25, blank=False)
    
    class Meta:
        db_table = "employee_account"
        
        
class RoleTableData(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=250, blank=False, unique=True)
    created_date = models.DateField(auto_now_add=True, editable=False)
    
    class Meta:
        db_table = "role"


class RolPermissionTableData(models.Model):
    role = models.ForeignKey(RoleTableData, on_delete=models.CASCADE)
    access = models.CharField(max_length=250, blank=False)
    permission = models.CharField(max_length=250, blank=False)
    
    class Meta:
        db_table = "role_permission"
        constraints = [
            models.UniqueConstraint(fields=['role', 'permission', 'access'], name='unique_role_permission')
        ]
    
    @classmethod
    def get_permissions_from_role(cls, role_id: str) -> List['RolPermissionTableData']:
        return [table for table in cls.objects.filter(role__id=role_id)]
    
    @classmethod
    def get_access_from_user(cls, user_id: str) -> Set[str]:
        user_access: Set[str] = set()
        roles = EmployeeRoleTableData.get_roles_from_employee(user_id)
        for role in roles:
            permissions = cls.get_permissions_from_role(role.id)
            user_access.update({permission.access for permission in permissions})
        return user_access


class EmployeeRoleTableData(models.Model):
    employee = models.ForeignKey(EmployeeAccountTableData, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleTableData, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, editable=False)
    
    @classmethod
    def get_roles_from_employee(cls, employee_id: str) -> List[RoleTableData]:
        tables = cls.objects.filter(employee__id=employee_id)
        return [table.role for table in tables]

    @classmethod
    def get_employees_from_role(cls, rolename: str) -> List[EmployeeAccountTableData]:
        tables = cls.objects.filter(role__name=rolename)
        return [table.employee for table in tables]
    
    class Meta:
        db_table = "employee_role"
        constraints = [
            models.UniqueConstraint(fields=['employee', 'role'], name='unique_employee_role')
        ]


class EmployeeCategoriesTableData(models.Model):
    employee = models.ForeignKey(EmployeeAccountTableData, on_delete=models.CASCADE)
    category = models.CharField(max_length=250, blank=False)
    
    @classmethod
    def get_categories_from_employee(cls, employee_id: str) -> List[str]:
        return [table.category for table in cls.objects.filter(employee__id=employee_id)]
    
    class Meta:
        db_table = "employee_categories"
        constraints = [
            models.UniqueConstraint(fields=['employee', 'category'], name='unique_employee_category')
        ]