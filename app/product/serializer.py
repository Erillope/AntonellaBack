from rest_framework import serializers
from core.product.service.dto import CreateProductDto, UpdateProductDto
from core.store_service.domain.values import ServiceType
from core.product.domain.values import ProductStatus

class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    stock = serializers.IntegerField()
    service_type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ServiceType])
    images = serializers.ListField(child=serializers.CharField())

    def to_dto(self) -> CreateProductDto:
        return CreateProductDto(
            name=self.validated_data['name'],
            price=self.validated_data['price'],
            description=self.validated_data['description'],
            stock=self.validated_data['stock'],
            service_type=self.validated_data['service_type'],
            images=self.validated_data['images']
        )


class UpdateProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    description = serializers.CharField(required=False)
    additional_stock = serializers.IntegerField(default=0)
    images = serializers.ListField(child=serializers.CharField(), required=False)
    service_type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ServiceType], required=False)
    status = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ProductStatus], required=False)
    
    def to_dto(self) -> UpdateProductDto:
        return UpdateProductDto(
            id=self.validated_data['id'],
            name=self.validated_data.get('name'),
            price=self.validated_data.get('price'),
            description=self.validated_data.get('description'),
            additional_stock=self.validated_data.get('additional_stock'),
            images=self.validated_data.get('images'),
            service_type=self.validated_data.get('service_type'),
            status=self.validated_data.get('status')
        )