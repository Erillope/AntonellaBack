from django.db import models
from app.user.models import UserAccountTableData
from core.payment.dto import DebitResponseDto

class UserCard(models.Model):
    card_id = models.CharField(max_length=255)
    user = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_card'
        constraints = [
            models.UniqueConstraint(fields=['id', 'user'], name='unique_user_card')
        ]

class DebitPayment(models.Model):
    transaction_id = models.CharField(max_length=255, primary_key=True)
    ok = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=255, unique=True)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    
    class Meta:
        db_table = 'debit_payment'
    
    @classmethod
    def save_payment(cls, payment_data: DebitResponseDto) -> None:
        cls.objects.create(
            transaction_id=payment_data.transaction_id,
            ok=payment_data.ok,
            amount=payment_data.amount,
            order_id=payment_data.order_id,
            taxable_amount=payment_data.taxable_amount,
            tax_percentage=payment_data.tax_percentage,
            user_card=UserCard.objects.get(user__id=payment_data.user_id),
            created_at=payment_data.created_at
        )