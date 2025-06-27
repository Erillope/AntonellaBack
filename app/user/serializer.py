from rest_framework import serializers
from core.user import AccountStatus, Gender
from core.common import OrdenDirection
from core.user.service.dto import SignUpDto, UpdateUserDto, FilterUserDto, CreateEmployeeDto
from core.user.domain.values import AccessType, PermissionType, RoleAccess, EmployeeCategories, PaymentType
from typing import List, Optional

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)
    

class EmployeeDataSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=250)
    roles = serializers.ListField(child=serializers.CharField(max_length=250))
    categories = serializers.ListField(
        child=serializers.ChoiceField(choices=[(c.value, c.value) for c in EmployeeCategories]),required=False)
    payment_type = serializers.ChoiceField(choices=[(p.value, p.value) for p in PaymentType])
    
    
class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=250)
    gender = serializers.ChoiceField(choices=[(g.value, g.value) for g in Gender])
    password = serializers.CharField(max_length=250)
    birthdate = serializers.DateField()
    employee_data = EmployeeDataSerializer(required=False)
    dni = serializers.CharField(max_length=250)
    photo = serializers.CharField(required=False)
    
    def to_dto(self) -> SignUpDto:
        if self.validated_data.get('employee_data'):
            return CreateEmployeeDto(
                phone_number=self.validated_data['phone_number'],
                email=self.validated_data['email'],
                name=self.validated_data['name'],
                gender=Gender(self.validated_data['gender']),
                password=self.validated_data['password'],
                birthdate=self.validated_data['birthdate'],
                address=self.validated_data['employee_data']['address'],
                roles=self.validated_data['employee_data']['roles'],
                categories=[
                    EmployeeCategories(category)
                    for category in self.validated_data['employee_data']['categories']
                ],
                payment_type=PaymentType(self.validated_data['employee_data']['payment_type']),
                dni=self.validated_data['dni'],
                photo=self.validated_data.get('photo'),
            )
        return SignUpDto(
            phone_number=self.validated_data['phone_number'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            gender=Gender(self.validated_data['gender']),
            password=self.validated_data['password'],
            birthdate=self.validated_data['birthdate'],
            dni=self.validated_data['dni'],
            photo=self.validated_data.get('photo'),
        )

    
class UpdateUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    phone_number = serializers.CharField(max_length=250, required=False)
    password = serializers.CharField(max_length=250, required=False)
    email = serializers.CharField(max_length=250, required=False)
    name = serializers.CharField(max_length=250, required=False)
    status = serializers.ChoiceField(choices=[(s.name, s.name) for s in AccountStatus], required=False)
    dni = serializers.CharField(max_length=250, required=False)
    address = serializers.CharField(max_length=250, required=False)
    photo = serializers.CharField(required=False)
    roles = serializers.ListField(child=serializers.CharField(max_length=250), required=False)
    birthdate = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=[(g.value, g.value) for g in Gender], required=False)
    categories = serializers.ListField(
        child=serializers.ChoiceField(choices=[(c.value, c.value) for c in EmployeeCategories]),required=False)
    payment_type = serializers.ChoiceField(choices=[(p.value, p.value) for p in PaymentType], required=False)
    
    def to_dto(self) -> UpdateUserDto:
        status = self.validated_data.get('status')
        return UpdateUserDto(
            id=str(self.validated_data['id']),
            password=self.validated_data.get('password'),
            phone_number=self.validated_data.get('phone_number'),
            email=self.validated_data.get('email'),
            name=self.validated_data.get('name'),
            status=AccountStatus(status) if status else None,
            dni=self.validated_data.get('dni'),
            address=self.validated_data.get('address'),
            photo=self.validated_data.get('photo'),
            roles=self.validated_data.get('roles'),
            birthdate=self.validated_data.get('birthdate'),
            gender=self.validated_data.get('gender'),
            categories=self.validated_data.get('categories'),
            payment_type=self.validated_data.get('payment_type')
        )


class FilterUserSerializer(serializers.Serializer):
    service_category = serializers.ChoiceField(
        choices=[(c.value, c.value) for c in EmployeeCategories], required=False)
    only_clients = serializers.BooleanField(default=False, required=False)
    name = serializers.CharField(max_length=250, required=False)
    exact_name = serializers.CharField(max_length=250, required=False)
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
    
    def to_dto(self) -> FilterUserDto:
        return FilterUserDto(
            service_category=self.validated_data.get('service_category'),
            only_clients=self.validated_data.get('only_clients', False),
            exact_name=self.validated_data.get('exact_name'),
            name=self.validated_data.get('name'),
            offset=self.validated_data.get('offset'),
            limit=self.validated_data.get('limit'),
        )
        

class AccessSerializer(serializers.Serializer):
    access = serializers.ChoiceField(choices=[(a.value, a.value) for a in AccessType])
    permissions = serializers.ListField(child=serializers.ChoiceField(
        choices=[(p.value, p.value) for p in PermissionType]
    ))


class CreateRoleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    accesses = serializers.ListField(child=AccessSerializer())
    
    def get_accesses(self) -> List[RoleAccess]:
        return [
            RoleAccess(
                access_type=AccessType(access['access']),
                permissions={PermissionType(permission) for permission in access['permissions']}
            )
            for access in self.validated_data['accesses']
        ]

class UpdateRoleSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=250, required=False)
    accesses = serializers.ListField(child=AccessSerializer(), required=False)
    
    def get_accesses(self) -> Optional[List[RoleAccess]]:
        if self.validated_data.get('accesses'):
            return [
                RoleAccess(
                    access_type=AccessType(access['access']),
                    permissions={PermissionType(permission) for permission in access['permissions']}
                )
                for access in self.validated_data['accesses']
            ]
        return None

class ResetPasswordSerializer(serializers.Serializer):
    token_id = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)