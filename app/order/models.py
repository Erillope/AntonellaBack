from django.db import models
from app.store_service.models import StoreServiceTableData
from app.product.models import ProductTableData
from app.user.models import EmployeeAccountTableData
from app.user.models import UserAccountTableData

class OrderTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    client = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    card_charge = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)
    status = models.CharField(max_length=50)
    progress_status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    client_confirmed = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    order_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'order_table'


class ServiceItemTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    order = models.ForeignKey(OrderTable, on_delete=models.CASCADE)
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    payment_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date_info_day = models.DateField()
    date_info_start_time = models.TimeField()
    date_info_end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'service_item_table'


class PaymentTable(models.Model):
    employee = models.ForeignKey(EmployeeAccountTableData, on_delete= models.SET_NULL, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_item = models.ForeignKey(ServiceItemTable, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'payment_table'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'service_item'], name='unique_employee_service_item')
        ]

    @classmethod
    def from_service_item(cls, service_item_id: str) -> 'PaymentTable':
        return cls.objects.filter(service_item__id=service_item_id)


class ProductItemTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    order = models.ForeignKey(OrderTable, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductTableData, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'product_item_table'
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]


class EmployeePaymentTable(models.Model):
    employee = models.ForeignKey(EmployeeAccountTableData, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employee_payment_table'