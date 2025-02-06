from rest_framework import serializers
from core.user import AccountStatus, Gender
from core.common import OrdenDirection
from core.user.service.dto import SignUpDto, UpdateUserDto, FilterUserDto
from datetime import date

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)
    
    
class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=250)
    name = serializers.CharField(max_length=250)
    gender = serializers.ChoiceField(choices=[(g.name, g.name) for g in Gender])
    password = serializers.CharField(max_length=250)
    birthdate = serializers.DateField()
    roles = serializers.ListField(child=serializers.CharField(max_length=250), required=False)
    
    @classmethod
    def to_dto(cls) -> SignUpDto:
        return SignUpDto(
            phone_number=cls.validated_data['phone_number'],
            email=cls.validated_data['email'],
            name=cls.validated_data['name'],
            gender=Gender(cls.validated_data['gender']),
            password=cls.validated_data['password'],
            birthdate=date.fromisoformat(cls.validated_data['birthdate']),
            roles=cls.validated_data['roles']
        )


class UpdateUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    phone_number = serializers.CharField(max_length=250, required=False)
    email = serializers.EmailField(max_length=250, required=False)
    name = serializers.CharField(max_length=250, required=False)
    password = serializers.CharField(max_length=250, required=False)
    status = serializers.ChoiceField(choices=[(s.name, s.name) for s in AccountStatus], required=False)
    
    @classmethod
    def to_dto(cls) -> UpdateUserDto:
        status = cls.validated_data.get('status')
        return UpdateUserDto(
            id=cls.validated_data['id'],
            phone_number=cls.validated_data.get('phone_number'),
            email=cls.validated_data.get('email'),
            name=cls.validated_data.get('name'),
            password=cls.validated_data.get('password'),
            status=AccountStatus(status) if status else None
        )


class FilterUserSerializer(serializers.Serializer):
    expresion = serializers.CharField(max_length=250, required=False)
    order_by = serializers.CharField(max_length=250)
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
    order_direction = serializers.ChoiceField(choices=[(o.name, o.name) for o in OrdenDirection], required=False)
    
    @classmethod
    def to_dto(cls) -> FilterUserDto:
        order_direction = cls.validated_data.get('order_direction')
        return FilterUserDto(
            expresion=cls.validated_data.get('expresion'),
            order_by=cls.validated_data['order_by'],
            offset=cls.validated_data.get('offset'),
            limit=cls.validated_data.get('limit'),
            order_direction=OrdenDirection(order_direction) if order_direction else None
        )