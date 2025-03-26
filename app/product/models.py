from django.db import models
from typing import List

class ProductTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(max_length=255)
    created_date = models.DateField()
    
    class Meta:
        db_table = 'product'


class ProductImage(models.Model):
    product = models.ForeignKey(ProductTableData, on_delete=models.CASCADE)
    image = models.TextField()
    
    class Meta:
        db_table = 'product_image'
    
    @classmethod
    def get_product_images(cls, product_id: str) -> List[str]:
        return [image.image for image in cls.objects.filter(product__id=product_id)]