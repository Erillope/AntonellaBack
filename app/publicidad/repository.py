from app.publicidad.models import PublicidadTable, PublicidadImage, ServicePublicidad, ProductPublicidad
from .mapper import PublicidadTableMapper
from app.common.django_repository import DjangoGetModel, DjangoSaveModel, DjangoDeleteModel
from core.common import Event, EventSubscriber
from core.publicidad.publicidad import Publicidad, ItemData
from core.publicidad.events import PublicidadSaved, PublicidadDeleted
from core.publicidad.repository import GetPublicidad
from typing import List

class DjangoGetPublicidad(DjangoGetModel[PublicidadTable, Publicidad], GetPublicidad):
    def __init__(self) -> None:
        super().__init__(PublicidadTable, PublicidadTableMapper())
    
    def get_related_publicidad(self, services_id: List[str], products_id: List[str]) -> List[Publicidad]:
        tables = PublicidadTable.get_publicidad_by_services_and_products(services_id, products_id)
        return [self.mapper.to_model(table) for table in tables]


class DjangoSavePublicidad(DjangoSaveModel[PublicidadTable, Publicidad], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(PublicidadTableMapper())
        EventSubscriber.__init__(self)

    def save(self, publicidad: Publicidad) -> None:
        super().save(publicidad)
        self.save_images(publicidad)
        self.save_service_items(publicidad)
        self.save_product_items(publicidad)
    
    def save_images(self, publicidad: Publicidad) -> None:
        PublicidadImage.objects.filter(publicidad_id=publicidad.id).delete()
        for image in publicidad.images:
            PublicidadImage.objects.create(publicidad_id=publicidad.id, image=image)
    
    def save_service_items(self, publicidad: Publicidad) -> None:
        ServicePublicidad.objects.filter(publicidad_id=publicidad.id).delete()
        for item in publicidad.service_items:
            ServicePublicidad.objects.create(publicidad_id=publicidad.id, 
                                             service_id=item.id, 
                                             discount=item.discount,
                                             fixed_amount=item.fixed_amount,
                                             type=item.type
                                                )
    
    def save_product_items(self, publicidad: Publicidad) -> None:
        ProductPublicidad.objects.filter(publicidad_id=publicidad.id).delete()
        for item in publicidad.product_items:
            ProductPublicidad.objects.create(publicidad_id=publicidad.id, 
                                             product_id=item.id, 
                                             discount=item.discount,
                                             fixed_amount=item.fixed_amount,
                                             type=item.type
                                                )

    def handle(self, event: Event) -> None:
        if isinstance(event, PublicidadSaved):
            self.save(event.publicidad)


class DjangoDeletePublicidad(DjangoDeleteModel[PublicidadTable, Publicidad], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(PublicidadTable, PublicidadTableMapper(), DjangoGetPublicidad())
        EventSubscriber.__init__(self)

    def delete(self, publicidad_id: str) -> Publicidad:
        PublicidadImage.objects.filter(publicidad_id=publicidad_id).delete()
        ServicePublicidad.objects.filter(publicidad_id=publicidad_id).delete()
        ProductPublicidad.objects.filter(publicidad_id=publicidad_id).delete()
        return super().delete(publicidad_id)

    def handle(self, event: Event) -> None:
        if isinstance(event, PublicidadDeleted):
            self.delete(event.publicidad.id)