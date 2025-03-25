from app.product.models import ProductImage, ProductTableData
from .mapper import ProductTableMapper
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from core.common import Event, EventSubscriber
from core.product import Product
from core.product.domain.events import ProductSaved, ProductDeleted

class DjangoGetProduct(DjangoGetModel[ProductTableData, Product]):
    def __init__(self) -> None:
        super().__init__(ProductTableData, ProductTableMapper())
    

class DjangoSaveProduct(DjangoSaveModel[ProductTableData, Product], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(ProductTableMapper())
        EventSubscriber.__init__(self)
    
    def save(self, product: Product) -> None:
        super().save(product)
    
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