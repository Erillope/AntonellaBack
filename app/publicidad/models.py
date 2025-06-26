from django.db import models
from app.store_service.models import StoreServiceTableData
from app.product.models import ProductTableData
from typing import List

class PublicidadTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField()

    class Meta:
        db_table = 'publicidad'


class PublicidadImage(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE, related_name='images')
    image = models.TextField()

    class Meta:
        db_table = 'publicidad_image'

    @classmethod
    def get_publicidad_images(cls, publicidad_id: str) -> list[str]:
        return [image.image for image in cls.objects.filter(publicidad__id=publicidad_id)]


class ServicePublicidad(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE, related_name='service_items')
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'service_publicidad'
    
    @classmethod
    def get_publicidad_services(cls, publicidad_id: str) -> List['ServicePublicidad']:
        return [sp for sp in cls.objects.filter(publicidad__id=publicidad_id)]


class ProductPublicidad(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE, related_name='product_items')
    product = models.ForeignKey(ProductTableData, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'product_publicidad'
    
    @classmethod
    def get_publicidad_products(cls, publicidad_id: str) -> List['ProductPublicidad']:
        return [pp for pp in cls.objects.filter(publicidad__id=publicidad_id)]