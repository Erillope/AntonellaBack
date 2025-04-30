from rest_framework import serializers
from core.payment.dto import DebitRequestDto

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
    card_id = serializers.CharField(max_length=100, required=True)
    user_id = serializers.CharField(max_length=100, required=True)