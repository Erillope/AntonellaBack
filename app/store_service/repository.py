from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.store_service.domain.store_service import StoreService
from .models import StoreServiceTableData, StoreServiceImage
from core.common import EventSubscriber, Event
from core.store_service.domain.events import (StoreServiceSaved, StoreServiceDeleted,
                                              StoreServiceImageAdded, StoreServiceImageDeleted)
from .mapper import StoreServiceTableMapper

class DjangoSaveStoreService(DjangoSaveModel[StoreServiceTableData, StoreService], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(StoreServiceTableMapper())
        EventSubscriber.__init__(self)
        
    def add_image(self, store_service_id: str, image: str) -> None:
        store_service = StoreServiceTableData.objects.get(id=store_service_id)
        StoreServiceImage.objects.create(image=image, service=store_service)
    
    def delete_image(self, store_service_id: str, image: str) -> None:
        store_service = StoreServiceTableData.objects.get(id=store_service_id)
        store_service_image = StoreServiceImage.objects.get(service=store_service, image=image)
        store_service_image.delete()
        
    def handle(self, event: Event) -> None:
        if isinstance(event, StoreServiceSaved):
            self.save(event.store_service)
        if isinstance(event, StoreServiceImageAdded):
            self.add_image(event.store_service_id, event.image.get_url())
        if isinstance(event, StoreServiceImageDeleted):
            self.delete_image(event.store_service_id, event.image_url)


class DjangoDeleteStoreService(DjangoDeleteModel[StoreServiceTableData, StoreService], EventSubscriber):
    def __init__(self) -> None:
        get_store_service = DjangoGetModel[StoreServiceTableData, StoreService](StoreServiceTableData, StoreServiceTableMapper())
        super().__init__(StoreServiceTableData, StoreServiceTableMapper(), get_store_service)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, StoreServiceDeleted):
            store_service = StoreServiceTableData.objects.get(id=event.store_service_id)
            self.delete(store_service)