from app.product.models import ProductImage, ProductTableData
from .mapper import ProductTableMapper
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from core.product.service.repository import GetProduct
from core.common import Event, EventSubscriber
from core.product import Product
from core.product.service.dto import ProductFilterDto
from core.product.domain.events import ProductSaved, ProductDeleted
from typing import List, Tuple
from django.db.models import Q

class DjangoGetProduct(DjangoGetModel[ProductTableData, Product], GetProduct):
    def __init__(self) -> None:
        super().__init__(ProductTableData, ProductTableMapper())
    
    def build_filter(self, dto: ProductFilterDto) -> Q:
        _filter = Q()
        if dto.name:
            _filter &= Q(name__icontains=dto.name)
        if dto.service_type:
            _filter &= Q(service_type=dto.service_type)
        if dto.start_stock_modified_date:
            _filter &= Q(stock_modified_date__gte=dto.start_stock_modified_date)
        if dto.end_stock_modified_date:
            _filter &= Q(stock_modified_date__lte=dto.end_stock_modified_date)
        return _filter
        
    def get_filtered_products(self, dto: ProductFilterDto) -> Tuple[List[Product], int]:
        _filter = self.build_filter(dto)
        products = self.table.objects.filter(_filter).distinct()
        product_count = products.count()
        if dto.only_count: [], product_count
        if dto.limit and dto.offset:
            products = products[dto.offset:dto.offset + dto.limit]
        elif dto.limit:
            products = products[:dto.limit]
        elif dto.offset:
            products = products[dto.offset:]
        return [self.mapper.to_model(p) for p in products], product_count
    

class DjangoSaveProduct(DjangoSaveModel[ProductTableData, Product], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ProductTableMapper())
        EventSubscriber.__init__(self)
    
    def save(self, product: Product) -> None:
        super().save(product)
        self.save_images(product)
    
    def save_images(self, product: Product) -> None:
        ProductImage.objects.filter(product_id=product.id).delete()
        for image in product.images:
            ProductImage.objects.create(product_id=product.id, image=image)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, ProductSaved):
            self.save(event.product)


class DjangoDeleteProduct(DjangoDeleteModel[ProductTableData, Product], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ProductTableData, ProductTableMapper(), DjangoGetProduct())
        EventSubscriber.__init__(self)
    
    def delete(self, product_id: str) -> Product:
        ProductImage.objects.filter(product_id=product_id).delete()
        return super().delete(product_id)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, ProductDeleted):
            self.delete(event.product.id)