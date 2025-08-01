from django.db import models
from app.store_service.models import StoreServiceTableData
from app.product.models import ProductTableData
from app.order.models import ServiceItemTable, ProductItemTable
from typing import List

class PublicidadTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField()
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'publicidad'
    
    @classmethod
    def get_publicidad_by_services_and_products(cls, services_id: List[str], products_id: List[str]) -> List['PublicidadTable']:
        tables = cls.objects.filter(enabled=True)
        filtered_tables = []
        for table in tables:
            publicidad_services = ServicePublicidad.get_publicidad_services(str(table.id))
            s_ids = [str(sp.service.id) for sp in publicidad_services]
            publicidad_products = ProductPublicidad.get_publicidad_products(str(table.id))
            p_ids = [str(pp.product.id) for pp in publicidad_products]
            if set(s_ids) == set(services_id) and set(p_ids) == set(products_id):
                filtered_tables.append(table)
        return filtered_tables


class PublicidadImage(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE)
    image = models.TextField()

    class Meta:
        db_table = 'publicidad_image'

    @classmethod
    def get_publicidad_images(cls, publicidad_id: str) -> list[str]:
        return [image.image for image in cls.objects.filter(publicidad__id=publicidad_id)]


class ServicePublicidad(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE)
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=10, default='descuento')

    class Meta:
        db_table = 'service_publicidad'
    
    @classmethod
    def get_publicidad_services(cls, publicidad_id: str) -> List['ServicePublicidad']:
        return [sp for sp in cls.objects.filter(publicidad__id=publicidad_id)]


class ProductPublicidad(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductTableData, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=10, default='descuento')

    class Meta:
        db_table = 'product_publicidad'
    
    @classmethod
    def get_publicidad_products(cls, publicidad_id: str) -> List['ProductPublicidad']:
        return [pp for pp in cls.objects.filter(publicidad__id=publicidad_id)]


class SelectedPublicidad(models.Model):
    publicidad = models.ForeignKey(PublicidadTable, on_delete=models.CASCADE)
    service_item = models.ForeignKey(ServiceItemTable, on_delete=models.CASCADE, null=True, blank=True)
    product_item = models.ForeignKey(ProductItemTable, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'selected_publicidad'