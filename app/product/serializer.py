from rest_framework import serializers
from core.product.service.dto import CreateProductDto, UpdateProductDto, ProductFilterDto
from core.store_service.domain.values import ServiceType
from core.product.domain.values import ProductStatus

class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    stock = serializers.IntegerField()
    service_type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ServiceType])
    service_subtype = serializers.CharField()
    product_type = serializers.CharField()
    volume = serializers.IntegerField()
    images = serializers.ListField(child=serializers.CharField())

    def to_dto(self) -> CreateProductDto:
        return CreateProductDto(
            name=self.validated_data['name'],
            price=self.validated_data['price'],
            description=self.validated_data['description'],
            stock=self.validated_data['stock'],
            service_type=self.validated_data['service_type'],
            service_subtype=self.validated_data['service_subtype'],
            product_type=self.validated_data['product_type'],
            volume=self.validated_data['volume'],
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
    service_subtype = serializers.CharField(required=False)
    product_type = serializers.CharField(required=False)
    volume = serializers.IntegerField(required=False)
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
            service_subtype=self.validated_data.get('service_subtype'),
            product_type=self.validated_data.get('product_type'),
            volume=self.validated_data.get('volume'),
            status=self.validated_data.get('status')
        )

class FilterProductSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    service_type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ServiceType], required=False)
    start_stock_modified_date = serializers.DateField(required=False)
    end_stock_modified_date = serializers.DateField(required=False)
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
    only_count = serializers.BooleanField(default=False)

    def to_dto(self) -> ProductFilterDto:
        return ProductFilterDto(
            name=self.validated_data.get('name'),
            service_type=self.validated_data.get('service_type'),
            start_stock_modified_date=self.validated_data.get('start_stock_modified_date'),
            end_stock_modified_date=self.validated_data.get('end_stock_modified_date'),
            limit=self.validated_data.get('limit'),
            offset=self.validated_data.get('offset'),
            only_count=self.validated_data['only_count']
        )