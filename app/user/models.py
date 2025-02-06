from core.user import AccountStatus, Gender
from django.db import models #type: ignore
from typing import List

class UserAccountTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    phone_number = models.CharField(max_length=250, blank=False, unique=True)
    email = models.EmailField(max_length=250, blank=False, unique=True)
    name = models.CharField(max_length=25, blank=False)
    password = models.CharField(max_length=250, blank=False)
    status = models.CharField(max_length=25, choices=[(s.name, s.name) for s in AccountStatus])
    gender = models.CharField(max_length=25, choices=[(g.name, g.name) for g in Gender])
    birthdate = models.DateField(blank=False)
    created_date = models.DateField(auto_now_add=True, editable=False)
    
    class Meta:
        db_table = "user_account"


class RoleTableData(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=250, blank=False, unique=True)
    created_date = models.DateField(auto_now_add=True, editable=False)
    
    class Meta:
        db_table = "role"


class UserRoleTableData(models.Model):
    user = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleTableData, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, editable=False)
    
    @classmethod
    def get_roles_from_user(cls, user_table: UserAccountTableData) -> List[RoleTableData]:
        user_role_tables = cls.objects.filter(user=user_table)
        return [table.role for table in user_role_tables]

    class Meta:
        db_table = "user_role"
        constraints = [
            models.UniqueConstraint(fields=['user', 'role'], name='unique_employee_role')
        ]