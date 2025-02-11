from django.db import models #type: ignore
from core.store_service import ServiceType, ServiceStatus

class StoreServiceTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[(s.value, s.value) for s in ServiceStatus])
    type = models.CharField(max_length=50, choices=[(t.value, t.value) for t in ServiceType])
    created_date = models.DateField()
    
    class Meta:
        db_table = 'store_service'
        
        
class StoreServiceImage(models.Model):
    image = models.TextField()
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'store_service_image'