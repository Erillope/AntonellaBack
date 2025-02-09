from rest_framework import serializers
from core.user import AccountStatus, Gender
from core.common import OrdenDirection
from core.user.service.dto import SignUpDto, UpdateUserDto, FilterUserDto

class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)
    
    
class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=250)
    gender = serializers.ChoiceField(choices=[(g.value, g.value) for g in Gender])
    password = serializers.CharField(max_length=250)
    birthdate = serializers.DateField()
    roles = serializers.ListField(child=serializers.CharField(max_length=250), required=False)
    
    def to_dto(self) -> SignUpDto:
        return SignUpDto(
            phone_number=self.validated_data['phone_number'],
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            gender=Gender(self.validated_data['gender']),
            password=self.validated_data['password'],
            birthdate=self.validated_data['birthdate'],
            roles=self.validated_data['roles']
        )


class UpdateUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    phone_number = serializers.CharField(max_length=250, required=False)
    email = serializers.CharField(max_length=250, required=False)
    name = serializers.CharField(max_length=250, required=False)
    status = serializers.ChoiceField(choices=[(s.name, s.name) for s in AccountStatus], required=False)
    
    def to_dto(self) -> UpdateUserDto:
        status = self.validated_data.get('status')
        return UpdateUserDto(
            id=str(self.validated_data['id']),
            phone_number=self.validated_data.get('phone_number'),
            email=self.validated_data.get('email'),
            name=self.validated_data.get('name'),
            status=AccountStatus(status) if status else None
        )


class FilterUserSerializer(serializers.Serializer):
    expresion = serializers.CharField(max_length=250, required=False)
    order_by = serializers.CharField(max_length=250)
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
    order_direction = serializers.ChoiceField(choices=[(o.name, o.name) for o in OrdenDirection], required=False)
    
    def to_dto(self) -> FilterUserDto:
        order_direction = self.validated_data.get('order_direction')
        return FilterUserDto(
            expresion=self.validated_data.get('expresion'),
            order_by=self.validated_data['order_by'],
            offset=self.validated_data.get('offset'),
            limit=self.validated_data.get('limit'),
            order_direction=OrdenDirection(order_direction) if order_direction else OrdenDirection.DESC
        )
