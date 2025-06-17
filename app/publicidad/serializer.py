from rest_framework import serializers
from core.publicidad.dto import CreatePublicidadDTO, UpdatePublicidadDTO
from core.publicidad.publicidad import ItemData

class ItemDataSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    
class CreatePublicidadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=1000, required=True)
    images = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    service_items = serializers.ListField(
        child=ItemDataSerializer(), required=True
    )
    product_items = serializers.ListField(
        child=ItemDataSerializer(), required=True
    )
    
    def get_service_items(self) -> list[ItemData]:
        item_datas: list[ItemData] = []
        for item in self.validated_data['service_items']:
            item_serializer = ItemDataSerializer(data=item)
            item_serializer.is_valid()
            item_datas.append(ItemData(id=item_serializer.validated_data['id'], discount=item_serializer.validated_data.get('discount')))
        return item_datas

    def get_product_items(self) -> list[ItemData]:
        item_datas: list[ItemData] = []
        for item in self.validated_data['product_items']:
            item_serializer = ItemDataSerializer(data=item)
            item_serializer.is_valid()
            item_datas.append(ItemData(id=item_serializer.validated_data['id'], discount=item_serializer.validated_data.get('discount')))
        return item_datas
    
    def to_dto(self) -> CreatePublicidadDTO:    
        return CreatePublicidadDTO(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            images=self.validated_data['images'],
            service_items=self.get_service_items(),
            product_items=self.get_product_items()
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
    
    def get_service_items(self) -> list[ItemData]:
        item_datas: list[ItemData] = []
        for item in self.validated_data.get('service_items'):
            item_serializer = ItemDataSerializer(data=item)
            item_serializer.is_valid()
            item_datas.append(ItemData(id=item_serializer.validated_data['id'], discount=item_serializer.validated_data.get('discount')))
        return item_datas

    def get_product_items(self) -> list[ItemData]:
        item_datas: list[ItemData] = []
        for item in self.validated_data.get('product_items'):
            item_serializer = ItemDataSerializer(data=item)
            item_serializer.is_valid()
            item_datas.append(ItemData(id=item_serializer.validated_data['id'], discount=item_serializer.validated_data.get('discount')))
        return item_datas
    
    def to_dto(self) -> UpdatePublicidadDTO:
        return UpdatePublicidadDTO(
            id=self.validated_data['id'],
            title=self.validated_data.get('title'),
            images=self.validated_data.get('images'),
            service_items=self.get_service_items() if 'service_items' in self.validated_data else None,
            product_items= self.get_product_items() if 'product_items' in self.validated_data else None
        )