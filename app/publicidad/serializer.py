from rest_framework import serializers
from core.publicidad.dto import CreatePublicidadDTO, UpdatePublicidadDTO
from core.publicidad.publicidad import ItemData, ItemType
from typing import Dict, Any

class ItemDataSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in ItemType], required=True)
    fixed_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    @classmethod
    def to_item_data(cls, data: Dict[str, Any]) -> ItemData:
        return ItemData(
            id=str(data['id']),
            type=ItemType(data['type']),
            fixed_amount=data.get('fixed_amount'),
            discount=data.get('discount')
        )
    
    @classmethod
    def to_item_data_list(cls, data_list: list[Dict[str, Any]]) -> list[ItemData]:
        return [cls.to_item_data(data) for data in data_list]
    
    
class CreatePublicidadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=True)
    images = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    service_items = serializers.ListField(
        child=ItemDataSerializer(), required=False
    )
    product_items = serializers.ListField(
        child=ItemDataSerializer(), required=False
    )
    
    def to_dto(self) -> CreatePublicidadDTO:    
        return CreatePublicidadDTO(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            images=self.validated_data['images'],
            service_items=ItemDataSerializer.to_item_data_list(self.validated_data['service_items']) if 'service_items' in self.validated_data else None,
            product_items=ItemDataSerializer.to_item_data_list(self.validated_data['product_items']) if 'product_items' in self.validated_data else None
        )


class UpdatePublicidadSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    title = serializers.CharField(max_length=255, required=False)
    images = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    service_items = serializers.ListField(
        child=ItemDataSerializer(), required=False
    )
    product_items = serializers.ListField(
        child=ItemDataSerializer(), required=False
    )
    enabled = serializers.BooleanField(required=False)
    
    def to_dto(self) -> UpdatePublicidadDTO:
        return UpdatePublicidadDTO(
            id=self.validated_data['id'],
            title=self.validated_data.get('title'),
            images=self.validated_data.get('images'),
            service_items=ItemDataSerializer.to_item_data_list(self.validated_data['service_items']) if 'service_items' in self.validated_data else None,
            product_items=ItemDataSerializer.to_item_data_list(self.validated_data['product_items']) if 'product_items' in self.validated_data else None,
            enabled=self.validated_data.get('enabled')
        )


class RelatedPublicidadSerializer(serializers.Serializer):
    services_id = serializers.ListField(
        child=serializers.UUIDField(), required=False, default=[]
    )
    products_id = serializers.ListField(
        child=serializers.UUIDField(), required=False, default=[]
    )

    def get_services_id(self) -> list[str]:
        return [str(service_id) for service_id in self.validated_data.get('services_id', [])]

    def get_products_id(self) -> list[str]:
        return [str(product_id) for product_id in self.validated_data.get('products_id', [])]


class AddPublicidadToItemSerializer(serializers.Serializer):
    publicidad_id = serializers.UUIDField(required=True)
    service_id = serializers.UUIDField(required=False, allow_null=True)
    product_id = serializers.UUIDField(required=False, allow_null=True)