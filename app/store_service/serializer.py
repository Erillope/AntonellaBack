from rest_framework import serializers
from core.store_service import ServiceType, ServiceStatus
from core.common import OrdenDirection
from core.store_service.service.dto import CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto

class CreateStoreSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField()
    type = serializers.ChoiceField(choices=[(t.value, t.value) for t in ServiceType])
    images = serializers.ListField(child=serializers.CharField(max_length=250))
    
    def to_dto(self) -> CreateStoreServiceDto:
        return CreateStoreServiceDto(
            name=self.validated_data['name'],
            description=self.validated_data['description'],
            type=ServiceType(self.validated_data['type']),
            images=self.validated_data['images']
        )


class UpdateStoreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=250, required=False)
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=[(s.name, s.name) for s in ServiceStatus], required=False)
    type = serializers.ChoiceField(choices=[(t.name, t.name) for t in ServiceType], required=False)
    
    def to_dto(self) -> UpdateStoreServiceDto:
        status = self.validated_data.get('status')
        return UpdateStoreServiceDto(
            id=str(self.validated_data['id']),
            name=self.validated_data.get('name'),
            description=self.validated_data.get('description'),
            status=ServiceStatus(status) if status else None,
            type=ServiceType(self.validated_data['type']) if self.validated_data.get('type') else None
        )


class FilterStoreServiceSerializer(serializers.Serializer):
    expresion = serializers.CharField(max_length=250, required=False)
    order_by = serializers.CharField(max_length=250)
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
    order_direction = serializers.ChoiceField(choices=[(o.name, o.name) for o in OrdenDirection], required=False)

    def to_dto(self) -> FilterStoreServiceDto:
        order_direction = self.validated_data.get('order_direction')
        return FilterStoreServiceDto(
            expresion=self.validated_data.get('expresion'),
            order_by=self.validated_data['order_by'],
            offset=self.validated_data.get('offset'),
            limit=self.validated_data.get('limit'),
            order_direction=OrdenDirection(order_direction) if order_direction else OrdenDirection.DESC
        )

class AddImageToStoreSerializer(serializers.Serializer):
    service_id = serializers.UUIDField()
    image = serializers.CharField(max_length=250)