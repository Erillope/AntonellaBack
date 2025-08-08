from rest_framework import serializers
from core.payment.dto import DebitRequestDto, AddUserCardDto, AddUserCardWithCardIdDto

class DebitPaymentSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=100, required=True)
    taxable_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    user_id = serializers.CharField(max_length=100, required=True)
    
    def to_dto(self) -> DebitRequestDto:
        return DebitRequestDto(
            order_id=self.validated_data['order_id'],
            taxable_amount=self.validated_data['taxable_amount'],
            user_id=self.validated_data['user_id']
        )


class AddUserCardSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    number = serializers.CharField(max_length=16, required=True)
    expiry_month = serializers.IntegerField(min_value=1, max_value=12, required=True)
    expiry_year = serializers.IntegerField(min_value=2000, required=True)
    cvc = serializers.CharField(max_length=4, required=True)

    def to_dto(self) -> AddUserCardDto:
        return AddUserCardDto(
            user_id=self.validated_data['user_id'],
            number=self.validated_data['number'],
            expiry_month=self.validated_data['expiry_month'],
            expiry_year=self.validated_data['expiry_year'],
            cvc=self.validated_data['cvc']
        )


class AddUserCardWithCardIdSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    card_id = serializers.CharField(max_length=100, required=True)

    def to_dto(self) -> AddUserCardWithCardIdDto:
        return AddUserCardWithCardIdDto(
            user_id=self.validated_data['user_id'],
            card_id=self.validated_data['card_id']
        )