from django.db import models
from app.store_service.models import StoreServiceTableData
from app.user.models import EmployeeAccountTableData

class OrderTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    client_id = models.UUIDField()
    card_charge = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    progress_status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    created_date = models.DateField()
    
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
    service_item = models.ForeignKey(ServiceItemTable, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'payment_table'
        constraints = [
            models.UniqueConstraint(fields=['employee', 'service_item'], name='unique_employee_service_item')
        ]

    @classmethod
    def from_service_item(cls, service_item_id: str) -> 'PaymentTable':
        return cls.objects.filter(service_item__id=service_item_id)